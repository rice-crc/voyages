Vue.component('v-toggle', {
  props: ['toggled', 'filter'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{filter.label}}</span>
        <span>
          <span class="fa toggle fa-control"
                v-bind:class="{'fa-toggle-on': toggledValue, 'fa-toggle-off': !toggledValue, 'primary-color': toggledValue, 'text-muted': !toggledValue}"
                @click="click">
          </span>
          <span class="toggle-label" v-show=false></span>
        </span><!-- reserved for right aligned content -->
      </div>
      <div class="v-description" v-text="filter.description"></div>

      <div class="row v-padding">
        <div class="col-md-12">
          <code>toggled: {{filter.value.searchTerm}}</code>
        </div>
      </div>
    </div>
  `,
  methods: {
    click() {
      this.filter.value.searchTerm = !this.filter.value.searchTerm;
    }
  },

  data: function() {
    if (this.toggled === undefined) {
      return {
        toggledValue: this.filter.default.searchTerm,
      }
    } else {
      return {
        toggledValue: this.toggled,
      }
    }

  },

  watch: {
    // update prop 'filter' from store
    filter: {
      handler: function(value){
        if (!this.filter.changed) { // update when filter is not activated
          this.toggledValue = this.filter.value.searchTerm;
        }
      },
      deep: true,
    }
  }
});
