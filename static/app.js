function toggleMenu(){
  var nav=document.getElementById('site-nav');
  var btn=document.querySelector('.menu-toggle');
  if(!nav) return;
  var open=nav.classList.contains('open');
  if(open){
    nav.classList.remove('open');
    if(btn) btn.setAttribute('aria-expanded','false');
  } else {
    nav.classList.add('open');
    if(btn) btn.setAttribute('aria-expanded','true');
  }
}

document.addEventListener('DOMContentLoaded', function(){
  var hero=document.querySelector('.hero');
  if(hero){
    hero.animate([
      {transform:'translateY(8px)', opacity:.9},
      {transform:'translateY(0)', opacity:1}
    ],{duration:500, easing:'ease-out'});
  }
  // form submit loading state
  window.handleGenerateSubmit=function(form){
    var btn=form.querySelector('.btn');
    if(btn){ btn.classList.add('loading'); }
    return true;
  };
  // fade-in on scroll
  var observer;
  if('IntersectionObserver' in window){
    observer=new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); observer.unobserve(e.target); } });
    },{threshold:0.12});
    document.querySelectorAll('.card').forEach(function(el){ observer.observe(el); });
  }
});


