// Generated by CoffeeScript 1.3.3
(function() {

  $(function() {
    var clickHandler;
    clickHandler = function(event) {
      var el, name, val;
      event.preventDefault();
      el = $(this);
      name = null;
      val = null;
      if (el.data('github') === 'tracked') {
        name = 'Track';
        val = 'untracked';
      } else {
        name = 'Untrack';
        val = 'tracked';
      }
      el.data('github', val);
      el.attr('data-github', val);
      el.toggleClass('btn-primary');
      el.parents('tr').toggleClass('tracked');
      return el.html(name);
    };
    return $('button[data-github]').click(clickHandler);
  });

}).call(this);
