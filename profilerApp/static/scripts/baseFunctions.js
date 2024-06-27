function convertFormToJSON(form) {
    const array = $(form).serializeArray();
    const json = {};
    $.each(array, function () {
      json[this.name] = this.value || "";
    });
    jsonConverted = JSON.stringify(json);
    return jsonConverted;
  }