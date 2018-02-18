Vue.component('v-toggle', {
  props: ['toggled','label'],
  template: `
    <div>
      {{ label }}
      <span class="fa toggle fa-control"
            v-bind:class="{'fa-toggle-on': toggled, 'fa-toggle-off': !toggled, 'primary-color': toggled, 'text-muted': !toggled}"
            @click="click">
      </span>
      <span class="toggle-label" v-show="label"></span>
    </div>
  `,
  methods: {
    click() {
      this.$emit('toggle', !this.toggled);
    }
  }
});
