// search js
$(function() {
	
	$( "#submit_search_product").on('click',function() {   
      var search_product = $( "#search_product" ).val();
      var csrf_token = $('#csrf_token').val();        
      var url = $('#search_url').val(); 
      var posting = $.post( url, {search_product:search_product,'csrfmiddlewaretoken': csrf_token} );
      // Put the results in a div
      posting.done(function( data ) {    
      $("#search_results" ).empty().append( data ); 
      // $('#modal_add_tax').modal(); 
      });
    
   });

});