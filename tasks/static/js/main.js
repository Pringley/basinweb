var list;
$(function() {
    'use strict';

    var Task = Backbone.Model.extend({});
    var TaskList = Backbone.Collection.extend({ model: Task })

    var ItemView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#item-template').html()),
        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
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

    var view = listViewFromUrl('/tasks/api/tasks/')
    $('#main-task-list').append(view.el);

});
