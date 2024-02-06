var schema_selector = document.getElementById("id_smart_data_model")
const element = document.getElementsByClassName("editor_holder")

if (!(element[0] instanceof Element)) {
    console.log(element[0])
    console.log("no")
  }

var editor = new JSONEditor(element[0],{
    display_required_only: true,
    disable_array_add: true , show_errors: 'never', ajax: true, theme: 'bootstrap3', schema: schema_selector.value})

$('document').ready(function() {
    $('#id_smart_data_model').on('change', function() {
        console.log(schema_selector.value);
        //const schema_dropdown = schema_selector.value
        editor.destroy();

        editor = new JSONEditor(element[0],{ajax: true, theme: 'bootstrap4',
            //schema: schema
            schema: JSON.parse(schema_selector.value)
        });
        editor.on('ready',() => {
      // Now the api methods will be available
        let errors = editor.validate();

    });


    editor.on('change',() => {
      // Now the api methods will be available
        let errors = editor.validate();
    });
    });

})
