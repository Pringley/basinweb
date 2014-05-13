// global app object
var app = app || {};

(function() {

    var STATES = ['active', 'delegated', 'blocked', 'sleeping', 'completed',
                  'trashed'];
    var ENTER_KEY = 13;
    var ESCAPE_KEY = 27;

    function cmp(x, y) {
        // standard compare:
        //      -1 means x comes first
        //       1 means y comes first
        //       0 means equal rank
        if (x === y)    { return 0; }
        else if (x < y) { return -1; }
        else            { return 1; }
    }

    function ncmp(x, y) {
        // null goes to the bottom
        if (x === null && y === null)   { return 0; }
        else if (x === null)            { return 1; }
        else if (y === null)            { return -1; }
        else                            { return cmp(x, y); }
    }

    function rncmp(x, y) {
        // null goes to the top
        if (x === null && y === null)   { return 0; }
        else if (x === null)            { return -1; }
        else if (y === null)            { return 1; }
        else                            { return cmp(x, y); }
    }


    function statecmp(s1, s2) {
        if (!_.contains(STATES, s1) || !_.contains(STATES, s2)) {
            throw "invalid state";
        }
        // compare by order defined in states variable
        var i1 = _.indexOf(STATES, s1),
            i2 = _.indexOf(STATES, s2);
        return cmp(i1, i2);
    }

    function sleepcmp(t1, t2) {
        var su1 = t1.get_dt('sleepuntil'),
            su2 = t2.get_dt('sleepuntil'),
            sf1 = t1.get('sleepforever'),
            sf2 = t2.get('sleepforever');
        // forever-sleeping tasks go to the bottom
        if (!sf1 && sf2) { return -1; }
        if (sf1 && !sf2) { return 1; }
        if (sf1 && sf2) { return 0; }
        // non-sleeping tasks (sleepuntil === null) go to top
        // otherwise, closer to wakeup goes to top
        return rncmp(su1, su2);
    }

    function taskcmp(t1, t2) {
        var state = t1.state();
        var state2 = t2.state();
        // compare by state if possible
        var r_state = statecmp(state, state2);
        var r_due = ncmp(t1.get_dt('due'), t2.get_dt('due'));
        if (r_state !== 0) { return r_state; }
        // otherwise choose order by shared state
        if (state === 'active' || state === 'deferred' || state === 'blocked') {
            if (r_due !== 0) { return r_due; }
            return rncmp(t1.get('summary'), t2.get('summary'));
        }
        if (state === 'sleeping') {
            if (r_due !== 0) { return r_due; }
            return sleepcmp(t1, t2);
        }
        if (state === 'completed' || state === 'trashed') {
            // latest modified first
            return -1 * cmp(t1.get_dt('modified'), t2.get_dt('modified'));
        }
        throw "invalid state";
    }

    var Task = Backbone.Model.extend({
        patch: function(attrs) {
            this.save(attrs, {patch: true});
        },
        toggle: function(field) {
            var attrs = {};
            attrs[field] = !this.get(field);
            this.patch(attrs);
        },
        sleepuntil: function(sleepuntil) {
            this.patch({ sleepuntil: sleepuntil, sleepforever: false });
        },
        unsleep: function() {
            this.patch({ sleepforever: false, sleepuntil: null });
        },
        delegateto: function(delegateto) {
            this.patch({ delegatedto: delegateto });
        },
        undelegate: function() {
            this.patch({ delegateto: ''});
        },
        get_mdt: function(field) {
            var raw = this.get(field);
            return raw === null ? null : new moment(raw);
        },
        get_mdt_human: function(field) {
            var mdt = this.get_mdt(field);
            return mdt === null ? null : mdt.fromNow();
        },
        get_dt: function(field) {
            var raw = this.get(field);
            return raw === null ? null : new Date(raw);
        },
        state: function() {
            var trashed = this.get('trashed'),
                completed = this.get('completed'),
                blockers = this.get('blockers'),
                sleepforever = this.get('sleepforever'),
                sleepuntil = this.get('sleepuntil'),
                delegatedto = this.get('delegatedto');
            if (trashed) { return 'trashed'; }
            if (completed) { return 'completed'; }
            if (blockers.length !== 0) { return 'blocked'; }
            if (sleepforever || (sleepuntil !== null &&
                        new Date(sleepuntil) > new Date()))
                { return 'sleeping'; }
            if (delegatedto !== '') { return 'delegated'; }
            return 'active';
        }
    });

    var Tasks = Backbone.Collection.extend({
        model: Task,
        url: "/api/tasks",
        comparator: taskcmp,
        filterState: function(state) {
            return new Tasks(this.filter(function(task) {
                return task.state() == state;
            }));
        }
    });

    var TaskView = Backbone.View.extend({
        tagName: 'div',
        template: _.template($('#task-template').html()),
        events: {
            'click .summary': 'editSummary',
            'blur .edit-summary': 'editSummaryReset',
            'keypress .edit-summary': 'editSummaryKeypress',
            'keydown .edit-summary': 'editSummaryKeydown',
            'click .due': 'editDue',
            'blur .edit-due': 'editDueReset',
            'keypress .edit-due': 'editDueKeypress',
            'keydown .edit-due': 'editDueKeydown',
            'click .complete-btn': 'completeBtn',
            'click .sleep-btn': 'sleepBtn',
            'click .delegate-btn': 'delegateBtn',
            'click .trash-btn': 'trashBtn'
        },
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },
        render: function () {
            this.$el.html(this.template({
                humandue: this.model.get_mdt_human('due'),
                task: this.model.toJSON()
            }));
            this.$el.addClass('task');
            this.$summary = this.$el.find('.summary');
            this.$editsummary = this.$el.find('.edit-summary');
            this.$due = this.$el.find('.due');
            this.$duedt = this.$due.find('.dt');
            this.$editdue = this.$el.find('.edit-due');
            this.$editsummary.hide();
            this.$editdue.hide();
            var state = this.model.state();
            if (state === 'delegated') {
                this.$el.find('.delegate-btn').html('Un-delegate');
            }
            else if (state === 'sleeping') {
                this.$el.find('.delegate-btn').hide();
                this.$el.find('.sleep-btn').html('Un-sleep');
            }
            else if (state === 'blocked') {
                this.$el.find('.delegate-btn').hide();
                this.$el.find('.sleep-btn').hide();
                this.$el.find('.block-btn').html('Un-block');
            }
            else if (state === 'completed') {
                this.$el.find('.sleep-btn').hide();
                this.$el.find('.block-btn').hide();
                this.$el.find('.delegate-btn').hide();
                this.$el.find('.complete-btn').html('Un-complete');
            }
            else if (state === 'trashed') {
                this.$el.find('.complete-btn').hide();
                this.$el.find('.sleep-btn').hide();
                this.$el.find('.block-btn').hide();
                this.$el.find('.delegate-btn').hide();
                this.$el.find('.trash-btn').html('Un-trash');
            }
        },

        editDue: function () {
            this.$duedt.hide();
            this.$editdue.show();
            this.$editdue.focus();
        },
        editDueDone: function () {
            var value = this.$editdue.val().trim();
            if (value === this.model.get('due')) {
                this.editDueReset();
                return;
            }
            this.model.patch({ due: value });
            this.render();
        },
        editDueReset: function(e) {
            this.$editdue.hide();
            this.$editdue.val(this.model.get('due'));
            this.$duedt.show();
        },
        editDueKeypress: function(e) {
            if (e.which === ENTER_KEY) { this.editDueDone(); }
        },
        editDueKeydown: function(e) {
            if (e.which === ESCAPE_KEY) {
                this.editDueReset();
            }
        },

        editSummary: function () {
            this.$summary.hide();
            this.$editsummary.show();
            this.$editsummary.focus();
        },
        editSummaryDone: function () {
            var value = this.$editsummary.val().trim();
            if (value === this.model.get('summary')) {
                this.editSummaryReset();
                return;
            }
            this.model.patch({ summary: value });
            this.render();
        },
        editSummaryReset: function(e) {
            this.$editsummary.hide();
            this.$editsummary.val(this.model.get('summary'));
            this.$summary.show();
        },
        editSummaryKeypress: function(e) {
            if (e.which === ENTER_KEY) { this.editSummaryDone(); }
        },
        editSummaryKeydown: function(e) {
            if (e.which === ESCAPE_KEY) {
                this.editSummaryReset();
            }
        },
        completeBtn: function () {
            this.model.toggle('completed');
            this.$el.remove();
        },
        trashBtn: function () {
            this.model.toggle('trashed');
            this.$el.remove();
        },
        delegateBtn: function () {
            if (this.model.state() === 'delegated') {
                this.model.undelegate();
            }
            else {
                var delegateto = prompt("delegate to:");
                this.model.delegateto(delegateto);
            }
            this.$el.remove();
        },
        sleepBtn: function () {
            if (this.model.state() === 'sleeping') {
                this.model.unsleep();
            }
            else {
                var sleepuntil = prompt("Sleep until:", (new Date()).toISOString());
                this.model.sleepuntil(sleepuntil);
            }
            this.$el.remove();
        },
    });

    var TasksView = Backbone.View.extend({
        render: function () {
            this.$el.html('');
            this.collection.each(function(task) {
                var taskView = new TaskView({model: task});
                taskView.render();
                this.$el.append(taskView.$el);
            }, this);
        }
    });

    var AppView = Backbone.View.extend({
        initialize: function() {
            _.each(STATES, function(state) {
                var btn = this.$el.find('.nav .' + state);
                var self = this;
                btn.on('click', function() {
                    app.router.navigate('state/' + state);
                    self.renderState(state);
                });
            }, this);
        },
        renderState: function(state) {
            var view = new TasksView({
                el: this.$el.find('.mainlist'),
                collection: app.tasks.filterState(state)
            });
            view.render();
        }
    });

    var Router = Backbone.Router.extend({
        routes: {
            "state/:state": "state"
        },
        state: function(state) {
            app.view.renderState(state);
        },
    });

    // initialize:
    app.tasks = new Tasks();
    app.router = new Router();
    app.view = new AppView({
        el: $('.app')
    });

    app.tasks.fetch().done(function() {
        app.view.renderState("active");
        Backbone.history.start();
    });


})();
