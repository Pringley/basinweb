var TASKS_URL = "/api/tasks/";

var state = 'active';
var states = ['active', 'sleeping', 'blocked', 'delegated', 'completed', 'trashed'];

function refresh(new_state) {
    var mainlist = $('.mainlist');
    mainlist.html('');
    $.ajax({
        url: "/api/tasks/"
    }).done(function(tasks) {
        state = new_state;
        _.each(tasks, function(task) {
            if (filters[state](task)) {
                var item = $('<li>').addClass('task');
                var contents = _.template($('#task-template').html(), {
                    task: task
                });
                item.html(contents);
                item.find('.complete-btn').click(function() {
                    $.ajax({
                        url: "/api/tasks/" + task.id + "/",
                        type: "PATCH",
                        data: { completed: !task.completed }
                    }).done(function() {
                        item.hide();
                    });
                });
                if (state === 'completed') {
                    item.find('.complete-btn').html('Un-complete')
                }
                mainlist.append(item);
            }
        });
    });
}

function highlightButton(new_state) {
    _.each(states, function(btnstate) {
        var button = $('.nav .' + btnstate);
        if (btnstate === new_state) {
            button.addClass('selected');
        }
        else {
            button.removeClass('selected');
        }
    });
}

var filters = {
    'active': function (task) {
        return !task.completed && !task.trashed && !task.sleepforever &&
            (task.sleepuntil === null || new Date(task.sleepuntil) <= new Date()) &&
            task.blockers.length === 0 && task.delegatedto === '';
    },
    'sleeping': function (task) {
        return !task.completed && !task.trashed && task.sleepforever ||
            (task.sleepuntil !== null && new Date(task.sleepuntil) > new Date());
    },
    'blocked': function (task) {
        return !task.completed && !task.trashed && task.blockers.length !== 0;;
    },
    'delegated': function (task) {
        return !task.completed && !task.trashed && task.delegatedto !== '';
    },
    'completed': function(task) {
        return task.completed && !task.trashed;
    },
    'trashed': function(task) {
        return task.trashed;
    }
}

$(function() {
    refresh('active');

    _.each(states, function(btnstate) {
        var button = $('.nav .' + btnstate);
        highlightButton(state);
        button.click(function() {
            refresh(btnstate);
            highlightButton(btnstate);
        });
    });
})
