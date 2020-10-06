
var hw = document.getElementById('hw');
hw.addEventListener('click', function(){
    alert('Hello world');
})


$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })