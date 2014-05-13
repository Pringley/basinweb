var TASKS_URL = "/api/tasks/";

var state = 'active';
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
                    var sleeping = filters['sleeping'](task);
                    var sleepuntil;
                    if (!sleeping) {
                        sleepuntil = prompt("Sleep until:", (new Date()).toISOString());
                    }
                    update_state(task, item,
                        !filters['sleeping'](task)
                            ? { sleepuntil: sleepuntil }
                            : { sleepuntil: null, sleepforever: false }
                    );
                });
                item.find('.delegate-btn')
                .click(function() {
                    var delegatedto;
                    if (task.delegatedto === '') {
                        delegatedto = prompt("Delegate to:");
                    }
                    update_state(task, item, {
                        delegatedto:
                            task.delegatedto === ''
                                ? delegatedto
                                : ''
                    });
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
