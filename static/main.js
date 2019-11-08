
// let question_mark = document.querySelector('.question_mark');
let token = document.querySelector('.token');
let howto = document.querySelector('.howto');
let title = document.querySelector('.title');
let description = document.querySelector('.description');



function showInstruction() {
	if (howto.style.display === 'block') {
		howto.style.display = 'none';
	} else {
		howto.style.display = 'block';
	}
}


function goTitle() {
	token.style.display = 'none';
	title.style.display = 'block';
}


function goDescription() {
	title.style.display = 'none';
	description.style.display = 'block';
}

function copyToClipboard() {
	let copyText = document.querySelector(".link");
	copyText.select();
	copyText.setSelectionRange(0, 99999)
	document.execCommand("copy");
}

// function copyToClipboard() {
// 	let span = document.querySelector('.link');
// 	console.log(span);
// 	span.select();
// 	// span.setSelectionRange(0, 99999)
// 	document.execCommand("copy");
// 	alert("Copied the text: " + span.value);
// 	let successful = document.execCommand('copy')
//     let msg = successful ? 'successfully' : 'unsuccessfully'	
// }