$ ->

	clickHandler = (event) ->
		event.preventDefault()

		el = $ @
		name = null
		val = null
		path = encodeURIComponent(el.parents('tr').find('a.repo-name:first').attr('href'))
		if el.data('github') is 'tracked'
			name = 'Track'
			val = 'untracked'

			$.delete("/repos/?path=#{path}")
		else
			name = 'Untrack'
			val = 'tracked'

			$.post("/repos/?path=#{path}")

		el.data 'github', val
		el.attr 'data-github', val
		el.toggleClass 'btn-primary'
		el.parents('tr').toggleClass 'tracked'
		el.html name
		

	$('button[data-github]').click clickHandler
