function convertFormToJSON(form) {
    const array = $(form).serializeArray();
    const json = {};
    $.each(array, function () {
      json[this.name] = this.value || "";
    });
    return JSON.stringify(json);
  }


  function getCsrfToken() {
    return $('meta[name="csrf-token"]').attr('content');
}