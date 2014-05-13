var TASKS_URL = "/api/tasks/";

var global_state = 'active';
var states = ['active', 'sleeping', 'blocked', 'delegated', 'completed', 'trashed'];

function update(task, fields) {
    return $.ajax({
        url: "/api/tasks/" + task.id + "/",
        type: "PATCH",
        data: fields
    })
}

function update_state(task, element, fields) {
    update(task, fields).done(function() {
        element.hide();
    });
}

function render_task(task, state) {
    var item = $('<li>').addClass('task');
    var contents = _.template($('#task-template').html(), {
        task: task
    });
    item.html(contents);
    item.find('.complete-btn')
    .click(function() {
        update_state(task, item, { completed: !task.completed });
    });
    item.find('.trash-btn')
    .click(function() {
        update_state(task, item, { trashed: !task.trashed });
    });
    item.find('.sleep-btn')
    .click(function() {
        if (state !== 'sleeping') {
            var sleepuntil = prompt("Sleep until:", (new Date()).toISOString());
            update_state(task, item, { sleepuntil: sleepuntil });
        }
        else {
            update_state(task, item, { sleepuntil: null, sleepforever: false });
        }
    });
    item.find('.delegate-btn')
    .click(function() {
        if (state !== 'delegated') {
            var delegatedto = prompt("Delegate to:");
            update_state(task, item, { delegatedto: delegatedto });
        }
        else {
            update_state(task, item, { delegatedto: '' });
        }
    });
    if (state === 'completed') {
        item.find('.sleep-btn').hide();
        item.find('.delegate-btn').hide();
        item.find('.complete-btn').html('Un-complete')
    }
    if (state === 'trashed') {
        item.find('.complete-btn').hide();
        item.find('.sleep-btn').hide();
        item.find('.delegate-btn').hide();
        item.find('.trash-btn').html('Un-trash')
    }
    if (state === 'delegated') {
        item.find('.delegate-btn').html('Un-delegate');
    }
    if (state === 'sleeping') {
        item.find('.sleep-btn').html('Un-sleep');
    }
    return item;
}

function refresh(state) {
    var mainlist = $('.mainlist');
    $.ajax({
        url: "/api/tasks/"
    }).done(function(tasks) {
        mainlist.html('');
        global_state = state;
        _.each(tasks, function(task) {
            if (filters[state](task)) {
                var item = render_task(task, state);
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
        highlightButton(global_state);
        button.click(function() {
            refresh(btnstate);
            highlightButton(btnstate);
        });
    });
})
