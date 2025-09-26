from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from .models import Blog
import re
import urllib.parse
import cohere
import random


def home(request: HttpRequest) -> HttpResponse:
    blogs = Blog.objects.order_by("-created_at")
    return render(request, "bloggen/home.html", {"blogs": blogs})


def blog_detail(request: HttpRequest, pk: int) -> HttpResponse:
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, "bloggen/detail.html", {"blog": blog})


def generate_blog(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        topic = request.POST.get("topic", "").strip()
        if not topic:
            return render(request, "bloggen/generate.html", {"error": "Please enter a topic."})

        api_key = getattr(settings, "COHERE_API_KEY", "")
        if not api_key:
            return render(request, "bloggen/generate.html", {"error": "Cohere API key is not configured."})

        co = cohere.Client(api_key)

        prompt = f"""
You are a seasoned human writer crafting a conversational blog post about: "{topic}".

Voice & style:
- Sound human: use contractions, varied sentence lengths, and natural rhythm.
- Show (brief) personal anecdotes or concrete examples.
- Avoid generic filler, avoid AI disclaimers, avoid repetition.
- Use simple words, occasional rhetorical questions, and warm, encouraging tone.
- Prefer concise paragraphs (3-5 sentences) with helpful specifics.


Structure:
- Catchy, specific title
- Short hook/intro (1 paragraph)
- 3–5 sections with <h2> headings and supporting paragraphs
- Key takeaways as a short bullet list
- Honest, encouraging conclusion

Output format with explicit sections:
TITLE: <title>
INTRO: <intro>
SECTIONS:
1) <h2>Heading</h2>\n<p>Paragraph with a concrete example or mini-anecdote...</p>
2) ...
TAKEAWAYS:
- item 1
- item 2
CONCLUSION: <conclusion>
"""

        try:
            chat_resp = co.chat(
                model="command-a-03-2025",
                message=prompt,
                max_tokens=800,
                temperature=0.6,
            )
            # SDK response compatibility handling
            text = ""
            if getattr(chat_resp, "text", None):
                text = chat_resp.text.strip()
            elif getattr(chat_resp, "message", None) and getattr(chat_resp.message, "content", None):
                blocks = chat_resp.message.content
                parts = []
                for b in blocks:
                    # Text or tool blocks; take text-like content
                    val = getattr(b, "text", None) or getattr(b, "content", None)
                    if val:
                        parts.append(str(val))
                text = "\n".join(parts).strip()
            else:
                text = ""
            if not text:
                raise RuntimeError("Empty response from Cohere Chat API")
        except Exception as exc:
            return render(request, "bloggen/generate.html", {"error": f"Cohere error: {exc}"})

        # Simple parse heuristics
        title = "Generated Blog"
        intro = ""
        sections_html = ""
        takeaways_html = ""
        conclusion = ""

        # Ensure markers land on their own lines even if model emits them inline
        text = re.sub(r"\s*(TITLE:|INTRO:|SECTIONS:|TAKEAWAYS:|CONCLUSION:)\s*", r"\n\1 ", text, flags=re.IGNORECASE)

        # Minimal markdown → HTML for bold/italic so ** and * render as expected
        def md_inline_to_html(s: str) -> str:
            if not s:
                return s
            # Convert inline markdown markers to HTML
            s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
            s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
            return s

        text = md_inline_to_html(text)

        # Drop stray lines that are only asterisks and trim dangling asterisks
        raw_lines = [l for l in text.splitlines()]
        lines = []
        for l in raw_lines:
            if re.fullmatch(r"\*+", l.strip()):
                continue
            # remove leading/trailing asterisks left by the model
            cleaned = re.sub(r"^\*+|\*+$", "", l.strip())
            if cleaned:
                lines.append(cleaned)
        current_section = None
        section_buffer = []

        def flush_section():
            nonlocal sections_html, section_buffer
            if section_buffer:
                for para in section_buffer:
                    if para:
                        sections_html += f"<p>{para}</p>\n"
                section_buffer = []

        for line in lines:
            upper = line.upper()
            if upper.startswith("TITLE:"):
                flush_section()
                title_val = line.split(":", 1)[1].strip().strip('"')
                title_val = re.sub(r"^\*+|\*+$", "", title_val).strip()
                title = title_val or title
            elif upper.startswith("INTRO:"):
                flush_section()
                intro_val = line.split(":", 1)[1].strip()
                intro_val = re.sub(r"^\*+|\*+$", "", intro_val).strip()
                intro = intro_val
            elif upper.startswith("SECTIONS:"):
                flush_section()
                current_section = "sections"
            elif upper.startswith("TAKEAWAYS:"):
                flush_section()
                current_section = "takeaways"
            elif upper.startswith("CONCLUSION:"):
                flush_section()
                current_section = "conclusion"
            else:
                if current_section == "takeaways":
                    item = re.sub(r"^[\-\*•–—]\s*", "", line).strip()
                    if item:
                        takeaways_html += f"<li>{item}</li>"
                elif current_section == "conclusion":
                    conclusion += (" " if conclusion else "") + line
                else:
                    # Convert numbered headings like "1) Title" or "2. Title" to <h2>
                    header_match = re.match(r"^\s*\d+[\.).]?\s*(.+)$", line)
                    if header_match:
                        flush_section()
                        heading = header_match.group(1).strip()
                        sections_html += f"<h2>{heading}</h2>\n"
                    elif line.lower().startswith("<h2>"):
                        flush_section()
                        sections_html += line + "\n"
                    else:
                        section_buffer.append(line)

        flush_section()

        content_parts = []
        if intro:
            content_parts.append(f"<p class=\"intro\">{intro}</p>")
        if sections_html:
            content_parts.append(f"<div class=\"sections\">{sections_html}</div>")
        if takeaways_html:
            content_parts.append(f"<div class=\"takeaways\"><h3>Key Takeaways</h3><ul>{takeaways_html}</ul></div>")
        if conclusion:
            content_parts.append(f"<p class=\"conclusion\">{conclusion}</p>")

        content_html = "\n".join(content_parts)

        # Topic-related cover image using Unsplash Source with a keyword query
        keywords = (title or topic or "blog").lower()
        query = urllib.parse.quote_plus(keywords)
        cover_image_url = f"https://source.unsplash.com/1200x600/?{query}"
        blog = Blog.objects.create(title=title, content=content_html, cover_image_url=cover_image_url)
        return redirect(reverse("blog_detail", args=[blog.pk]))

    return render(request, "bloggen/generate.html")

# Create your views here.
