$(document).ready(function() {
  // Fetch tasks on page load
  fetchTasks();

  // Submit form to create new task
  $('#createTaskForm').submit(function(e) {
    e.preventDefault();

    const title = $('#title').val();
    const description = $('#description').val();
    const status = $('#status').val();
    const priority = $('#priority').val();
    const due_date = $('#due_date').val();

    // Send AJAX request to create task
    $.ajax({
      url: '/api/tasks/create/',
      method: 'POST',
      data: {
        title: title,
        description: description,
        status: status,
        priority: priority,
        due_date: due_date,
      },
      success: function(response) {
        // Handle successful creation (e.g., clear form, update task list)
        $('#createTaskForm').trigger('reset');
        $('#createTaskModal').modal('hide');
        fetchTasks();
      },
      error: function(error) {
        console.error('Error creating task:', error);
        // Handle errors (e.g., display error message)
      },
    });
  });

  // Search functionality
  $('#search-bar').keyup(function() {
    const searchTerm = $(this).val().toLowerCase();
    $('#task-list li').each(function() {
      const taskTitle = $(this).find('h5').text().toLowerCase();
      if (taskTitle.indexOf(searchTerm) !== -1) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });

  // Edit task functionality (optional)
  // ... (implement logic to edit task details using AJAX)

  // Delete task functionality (optional)
  // ... (implement logic to delete task using AJAX)

  function fetchTasks() {
    $.ajax({
      url: '/api/tasks/',
      method: 'GET',
      success: function(data) {
        // Clear existing task list
        $('#task-list').empty();

        // Loop through task data and create list items
        data.data.forEach(function(task) {
          const listItem = $('<li class="p-2 border-b border-gray-200 task-item">');
          listItem.append($('<h5>' + task.title + '</h5>'));
          listItem.append($('<p>' + task.description + '</p>'));
          listItem.append($('<span class="badge bg-'+ (task.status === 'COMPLETED' ? 'green' : task.status === 'IN_PROGRESS' ? 'blue' : 'red') + ' text-white">' + task.status + '</span>'));
          listItem.append($('<span class="badge bg-'+ (task.priority === 'HIGH' ? 'red' : task.priority === 'MEDIUM' ? 'orange' : 'yellow') + ' text-white">' + task.priority + '</span>'));
          // Add due date element (optional)
          $('#task-list').append(listItem);
        });
      },
      error: function(error) {
        console.error('Error fetching tasks:', error);
        // Handle errors (e.g., display error message)
      },
    });
  }
});
 