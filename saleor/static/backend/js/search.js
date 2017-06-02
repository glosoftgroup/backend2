// search js
$(function() {
	alert('tafuta');
	$( "#submit_search_product").on('click',function() {   
    var search_product = $( this ).val();
         
      {% url "dashboard:search-product" as url %} 
      var url = "{{ url }}";
      var posting = $.post( url, {search_product:search_product} );
      // Put the results in a div
      posting.done(function( data ) {    
      // $("#add_tax_form" ).empty().append( data ); 
      // $('#modal_add_tax').modal(); 
      });
    
   });
});