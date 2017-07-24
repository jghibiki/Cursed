// a hack to make textareas resize automatically
// if updated via javascript call $('textarea').trigger('input'); to update 
//$('textarea').each(function () {
//  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
//}).on('input', function () {
//  this.style.height = 'auto';
//  this.style.height = (this.scrollHeight) + 'px';
//});


// a hacky function to download a file made from text converted to a data uri
function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
