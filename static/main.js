let howto = document.querySelector('.howto');


function showInstruction() {
	if (howto.style.display === 'block') {
		howto.style.display = 'none';
	} else {
		howto.style.display = 'block';
	}
}

function copyToClipboard() {
	let copyText = document.querySelector(".link");
	copyText.select();
	copyText.setSelectionRange(0, 99999)
	document.execCommand("copy");
}

