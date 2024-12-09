function agregarProducto(libroId) {
    const form = document.getElementById(`form-agregar-${libroId}`);
    form.submit();
  }
  
  function restarProducto(libroId) {
    const form = document.getElementById(`form-restar-${libroId}`);
    form.submit();
  }
  
  function eliminarProducto(libroId) {
    const form = document.getElementById(`form-eliminar-${libroId}`);
    form.submit();
  }
  