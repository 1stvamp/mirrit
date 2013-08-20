$ ->

	clickHandler = (event) ->
		event.preventDefault()

		el = $ @
		name = null
		val = null
		if el.data('github') is 'tracked'
			name = 'Track'
			val = 'untracked'
		else
			name = 'Untrack'
			val = 'tracked'

		el.data 'github', val
		el.attr 'data-github', val
		el.toggleClass 'btn-primary'
		el.parents('tr').toggleClass 'tracked'
		el.html name
		

	$('button[data-github]').click clickHandler
