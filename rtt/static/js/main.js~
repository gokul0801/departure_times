$(document).ready(function() {
  $("#agency").change(function() {
        var agency = $(this).val();
        $.post('ajax/getRoutes/',
	       {'agency' : agency} , 
	       function(data, status) {
	         $("#route")
			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Route</option>');

 		 $("#direction")
			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Direction</option>');
		 $("#direction").show();
	         $('label[for="direction"]').show();
	         $("#direction").prop("disabled", true);
	         
		 $("#stop")
  			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Stop</option>');
	         $("#stop").prop("disabled", true);
                 
                 var routes = data.routes
	         $.each(routes, function(index, element) {
	           $("#route").append($('<option>', {
		     value: element.route,
	             text: element.route
		     }));
	         });
	         $("#route").prop('disabled', false);
                
                 if (data.hasDirection == "False") {
		      $("#direction").hide();
	              $('label[for="direction"]').hide();
	          }
	        },
	       'json');
    });

  $("#route").change(function() {
	var agency = $("#agency").val();
	var route = $("#route").val();
	if ($("#direction").is(":visible")) {
	   $.post('ajax/getDirections/',
	         {'agency': agency, 'route': route},
	         function(data, status) {
		   $("#direction")
			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Direction</option>');
		    $.each(data, function(index, element) {
	               $("#direction").append($('<option>', {
		      	 value: element.direction,
		       	 text: element.direction
                        }));
	            });
                   $("#direction").prop('disabled', false);
	         },
	         'json');
      } else {
	var agency = $("#agency").val();
	var route = $("#route").val();
        $.post('ajax/getStops/',
	       {'agency': agency, 'route': route},
	       function(data, status) {
	         $("#stop")
  			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Stop</option>');
 		  $.each(data, function(index, element) {
	               $("#stop").append($('<option>', {
		      	 value: element.stop,
		       	 text: element.stop
                        }));
	            });
                   $("#stop").prop('disabled', false);
	         },
	         'json');
	}
   });

  $("#direction").change(function() {
	var agency = $("#agency").val();
	var route = $("#route").val();
        var direction = $("#direction").val();
	$.post('ajax/getStops/',
	       {'agency': agency, 'route': route, 'direction': direction},
	       function(data, status) {
	         $("#stop")
  			.find('option')
		        .remove()
		        .end()
	                .append('<option>Select a Stop</option>');
 		  $.each(data, function(index, element) {
	               $("#stop").append($('<option>', {
		      	 value: element.stop,
		       	 text: element.stop
                        }));
	            });
                   $("#stop").prop('disabled', false);
	         },
	         'json');
   });                 

  $("#startover").click(function() {
	$("#agency").val("Select an Agency");
	$("#route").find('option')
		    .remove()
		    .end()
	            .append('<option>Select a Route</option>');
	$("#route").prop("disabled", true);
        $("#direction").find('option')
		      .remove()
		      .end()
	              .append('<option>Select a Direction</option>');
        $("#direction").show();
	$('label[for="direction"]').show();
	$("#direction").prop("disabled", true);
	         
        $("#stop").find('option')
		  .remove()
		  .end()
	          .append('<option>Select a Stop</option>');
	$("#stop").prop("disabled", true);
   });


});

