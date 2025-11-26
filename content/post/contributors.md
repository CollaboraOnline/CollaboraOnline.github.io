
+++
authors = [
    "Collabora",
]
title = "Contributors & Supporters"
date = "2023-07-04"
home_pos = "14"
description = "COOL Contributors"
tags = [
    "build",
    "make",
]
images = [
    "beaver/contributors-copyrighted.png",
]

showimage = false
showtitle = true
+++

<div class="contributors-intro-wrapper">
    <div class="contributors-intro-text">
        <p>Thank you to everyone who helps move the COOL project forward!</p>
        <!--more-->
        <p>This page highlights the amazing people and organizations who contribute their time,
        expertise, and support. Use the tabs below to see our individual contributors and
        our valued supporters.</p>
    </div>

<img src="../../images/beaver/pookie-beaver.png"
     alt="Contributors Beaver Artwork"
     class="contributors-beaver">
</div>

<link rel="stylesheet" href="/css/contributors-tabs.css">

<div class="tabs" role="tablist" aria-label="Contributors navigation">
    <button class="tab-button active" role="tab" aria-selected="true" data-tab="contributors">Contributors</button>
    <button class="tab-button" role="tab" aria-selected="false" data-tab="supporters">Supporters</button>
</div>

<div id="contributors-section" class="tab-section tab-fade">

<!-- CONTRIBUTORS-START -->

{{< contributors-list >}}

<!-- CONTRIBUTORS-END -->
</div>

<div id="supporters-section" class="tab-section" aria-hidden="true" style="padding:20px 0; text-align:center;">
<!-- SUPPORTERS-START -->
{{< supporters-list >}}
<!-- SUPPORTERS-END -->
</div>

<script>
document.addEventListener('DOMContentLoaded', function(){
    const buttons = document.querySelectorAll('.tab-button');
    const contrib = document.getElementById('contributors-section');
    const supp = document.getElementById('supporters-section');
    function activate(tab){
        buttons.forEach(b=>{
            const is = b.dataset.tab===tab;
            b.classList.toggle('active', is);
            b.setAttribute('aria-selected', is? 'true' : 'false');
        });
        if(tab==='contributors'){
            contrib.style.display = 'block';
            supp.style.display = 'none';
        } else {
            contrib.style.display = 'none';
            supp.style.display = 'block';
        }
    }
    buttons.forEach(b=> b.addEventListener('click', ()=> activate(b.dataset.tab)));
    // keep initial state consistent
    activate(document.querySelector('.tab-button.active')?.dataset.tab || 'contributors');
});
</script>
