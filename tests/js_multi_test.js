<script type="text/javascript" src="http://benjamingolder.com/static/js/jquery.min.js"></script>
<script type="text/javascript">
$(function(){
	var panel = $('<div id="panel" class="hide"></div>');
	$('#container').append(panel);
	$('path').hover(function(e){
		var text = $(this).attr('text');
		var x = e.offsetX;
		var y = e.offsetY;
		panel.removeClass('hide');
		panel.html(text);
		panel.offset({top:y, left:x + 24});
	});
	$('path').mouseleave(function(e){
		panel.addClass('hide');
	});
})
        </script>
