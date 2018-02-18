Vue.component('v-toggle', {
  props: ['title', 'description', 'toggled', 'label'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{title}}</span>
        <span>
          <span class="fa toggle fa-control"
                v-bind:class="{'fa-toggle-on': toggled, 'fa-toggle-off': !toggled, 'primary-color': toggled, 'text-muted': !toggled}"
                @click="click">
          </span>
          <span class="toggle-label" v-show="label"></span>
        </span><!-- reserved for right aligned content -->
      </div>
      <div class="v-description" v-text="description"></div>

      <div class="row v-padding">
        <div class="col-md-12">
          <code>toggled: {{toggled}}</code>
        </div>
      </div>
    </div>
  `,
  methods: {
    click() {
      this.$emit('toggle', !this.toggled);
    }
  }
});
