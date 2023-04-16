var modal = document.querySelector(".modal");
var trigger = document.querySelector(".trigger");
var closeButton = document.querySelector(".close-button");

function toggleModal() {
    modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal();
    }
}

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);


function SUB(){
		document.getElementById('GFG').submit();
	}

function okay(){
	    if ((document.getElementsByClassName("text-field__input")[0].value != '') && (document.getElementsByClassName("text-field__input")[1].value != '') && (document.getElementsByClassName("text-field__input")[2].value != '')){
    		document.getElementById('well').innerHTML = '<svg id="svg1" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  width="94" height="94" viewBox="0 0 47 47"  > <circle fill="transparent" cx="24" cy="24" r="21"/> <path class="path" fill= "none" stroke ="#44944A" stroke-width ="1.5" stroke-dasharray= "70.2" stroke-dashoffset="70.2"  d="M 34.6 14.6  L 21 28.2 L 15.4 22.6 L 12.6 25.4 L 21 33.8 L 37.4 17.4z"> <animate id="p1" attributeName="stroke-dashoffset" begin="0.2s" values="70.2;0" dur="2s" repeatCount="1" fill="freeze" calcMode="paced" restart="whenNotActive"/>  <animate id="f1" attributeName="fill" begin = "p1.end" values="transparent"  dur="1s" fill="freeze" restart="whenNotActive" />  </path> </svg>';
    		document.getElementById('GFG').style.display = 'none';
    		document.getElementById('ostav').style.display = 'none';
    		setTimeout(SUB, 500);
	    }
		
	}