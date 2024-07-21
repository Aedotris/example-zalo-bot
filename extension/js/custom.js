function copyTextToClipboard(str, options) {
  const el = document.createElement('textarea');
  el.value = str;
  el.setAttribute('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
}

document.getElementById('btn-copy-1').addEventListener('click', async () => {
  var textInput = document.getElementById("imei");
  if (!textInput.value) return;

  copyTextToClipboard(textInput.value);

  let btnCopy = document.getElementById('btn-copy-1');

  btnCopy.innerText = "Copied";
  let timeoutCopy = setTimeout(() => {
    btnCopy.innerHTML = `<i class="el-icon-document-copy"></i>`;
    clearTimeout(timeoutCopy);
  }, 2000);
});

document.getElementById('btn-copy-2').addEventListener('click', async () => {
  var textInput = document.getElementById("cookies");
  if (!textInput.value) return;

  copyTextToClipboard(textInput.value);

  let btnCopy = document.getElementById('btn-copy-2');

  btnCopy.innerText = "Copied";
  let timeoutCopy = setTimeout(() => {
    btnCopy.innerHTML = `<i class="el-icon-document-copy"></i>`;
    clearTimeout(timeoutCopy);
  }, 2000);
});

document.addEventListener("DOMContentLoaded", function() {
	document.getElementById("refresh-button").addEventListener("click", function() {
		chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
			chrome.tabs.reload(tabs[0].id);
		});
	});
});