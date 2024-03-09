// Handle the edit task modal. 
$(document).ready(function () {
  $('.edit-task-btn').click(function () {
      var taskId = $(this).closest('.card').find('.card-title').attr('id').split('-')[1];
      var taskContent = $('#content-' + taskId).text().trim();
      $('#edit_task_modal-' + taskId + ' input[name="new_content"]').val(taskContent);
  });
});