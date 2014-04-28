$(function() {
    var Task = Backbone.Model.extend({});

    var TaskList = Backbone.Collection.extend({
        model: Task,
        url: '/api/tasks/'
    });

    var TaskView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#task-template').html()),
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    var AppView = Backbone.View.extend({
        el: $('#task-app'),
        initialize: function() {
            this.tasks = new TaskList();
            this.listenTo(this.tasks, 'add', this.addOne);
            this.tasks.fetch();
        },
        addOne: function(task) {
            var view = new TaskView({model: task});
            this.$('#task-list').append(view.render().el);
        }
    });

    var App = new AppView();
});
