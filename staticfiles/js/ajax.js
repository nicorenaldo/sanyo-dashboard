const user_input = $("#user-input")
const user_input2 = $("#user-input2")
const user_input3 = $("#user-input3")
const user_input4 = $("#user-input4")
const user_input5 = $("#user-input5")
const search_icon = $('#search-icon')
const div = $('#replaceable-content')
const endpoint = '/'
const delay_by_in_ms = 400
let scheduled_function = false
// var divv =  document.getElementByClass("activez")

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			div.fadeTo('fast', 0).promise().then(() => {
				// replace the HTML contents
				div.html(response['html_from_view'])
				
				// fade-in the div with new contents
				div.fadeTo('fast', 1)
				document.getElementById("defaultOpen").click();
				
				
			})
			
		})
	
}


user_input.on('keyup', function () {

	const request_parameters = {
		q: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// start animating the search icon with the CSS class
	search_icon.addClass('blink')

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

user_input2.click(function() {

	const request_parameters = {
		harga: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

user_input3.click(function() {

	const request_parameters = {
		harga: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

user_input4.click(function() {

	const request_parameters = {
		nama: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})


user_input5.click(function() {

	const request_parameters = {
		nama: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
