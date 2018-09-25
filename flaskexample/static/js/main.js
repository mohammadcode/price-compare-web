      $(document).ready(function() {
        $('#category').change(function() {
          var category = $('#category').val();
          $.getJSON('/get_sub_category' + '/' + category,
            function(data) {
              // Remove old options
              $('#sub_category').find('option').remove();                                
              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val.name + '">' + val.name + '</option>'
                $('#sub_category').append(option_item);
              });
            }
          );
        });
      });
