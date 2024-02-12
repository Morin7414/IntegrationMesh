// static/myapp/workorder_admin.js

(function($) {
    $(document).ready(function() {

        var previousValue = $('#id_machine').val(); // Store the initial value

        // Function to check if the value of the text field has changed
        function checkForChange() {
            var currentValue = $('#id_machine').val();
            if (currentValue !== previousValue) {
                previousValue = currentValue; // Update the previous value
                populateFields(); // Call the function to populate fields
            }
        }



        // Function to populate fields based on selected machine
        function populateFields() {
            var machineId = $('#id_machine').val();
            if (!machineId) {
                return;
            }

            // Make an AJAX request to fetch machine details
            $.ajax({
                url: '/get_machine_details/',  // URL to fetch machine details, update as needed
                data: {
                    'machine_id': machineId
                },
                dataType: 'json',
                success: function(data) {
                    // Populate fields with retrieved data
                    $('#id_asset_number').val(data.asset_number);
                    $('#id_location').val(data.location);
                    $('#id_model').val(data.model);
                 
                }
            });
        }

        // Bind the function to the change event of the machine field
       // $('#id_machine').change(populateFields);
     //   $('#id_machine').on('input', populateFields);
         // Create a MutationObserver instance
        setInterval(checkForChange, 500);


        // If machine is pre-selected (e.g., during edit), populate fields on page load
        if ($('#id_machine').val()) {
            populateFields();
        }
    });
})(jQuery);