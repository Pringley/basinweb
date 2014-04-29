var list;
$(function() {
    'use strict';

    var Task = Backbone.Model.extend({
        toggle_complete: function() {
            this.save({completed: !this.get("completed")}, {patch: true});
        }
    });
    var TaskList = Backbone.Collection.extend({ model: Task })

    var ItemView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#item-template').html()),
        events: {
            'click .done-button': 'toggle_complete',
        },
        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
        },
        toggle_complete: function() {
            this.model.toggle_complete();
        }
    });

    var ListView = Backbone.View.extend({
        tagName: 'ul',
        initialize: function() {
            this.listenTo(this.model, 'all', this.render);
        },
        addItem: function(item) {
            var view = new ItemView({model: item});
            this.$el.append(view.el);
        },
        render: function() {
            this.$el.html('');
            this.model.each(this.addItem, this);
        }
    });

    var listViewFromUrl = function(url) {
        var list = new TaskList();
        list.url = url;
        var view = new ListView({model: list});
        list.fetch({reset: true});
        return view;
    };

    var active = listViewFromUrl('/api/active/')
    var sleeping = listViewFromUrl('/api/sleeping/')
    var blocked = listViewFromUrl('/api/blocked/')
    var delegated = listViewFromUrl('/api/delegated/')
    var completed = listViewFromUrl('/api/completed/')
    $('#active-tasks').append(active.el);
    $('#sleeping-tasks').append(sleeping.el);
    $('#blocked-tasks').append(blocked.el);
    $('#delegated-tasks').append(delegated.el);
    $('#completed-tasks').append(completed.el);

});
