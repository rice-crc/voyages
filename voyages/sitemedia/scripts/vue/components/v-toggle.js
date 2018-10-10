Vue.component('v-toggle', {
  props: ['filter'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{filter.label}}</span>
        <span>
            
            <b-badge pill
              v-if="filter.options.isImputed"
              v-b-tooltip.hover title="Calculated by an algorithm and not based on historical record."
              variant="secondary"
              class="v-badge-imputed">
              IMPUTED
            </b-badge>
            
            <!--
            <b-badge
              v-if="filter.options.isAdvanced"
              v-b-tooltip.hover title="Advanced variables are additional parameters that are frequenlty used. They do not change current search behavior."
              variant="danger" class="v-badge-advanced">Advanced</b-badge>
            -->
        </span><!-- reserved for right aligned content -->
      </div>

      <div class="v-toggle-control">
        <span class="v-panel-description">{{filter.description}}</span>
        <span class="fa toggle fa-control"
              v-bind:class="{'fa-toggle-on': item.searchTerm, 'fa-toggle-off': !item.searchTerm, 'primary-color': item.searchTerm, 'text-muted': !item.searchTerm}"
              @click="click">
        </span><!-- reserved for right aligned content -->
      </div>

      <div class="row v-padding" v-if="false">
        <div class="col-md-12">
          <div>
            <code>{{item}}</code>
          </div>
          <div>
            <b-button :disabled="!options.changed" variant="success" size="sm" @click="apply">Apply</b-button>
            <b-button :disabled="!options.changed" variant="secondary" size="sm" @click="reset">Reset</b-button>
          </div>
        </div>
      </div>

    </div>
  `,
  methods: {
    click() {
      this.item.searchTerm = !this.item.searchTerm;
    },

    // form action buttons
    apply() {
      var searchString = JSON.stringify(this.item);
      alert(searchString);
    },

    reset() {
      this.item.searchTerm = this.filter.default.searchTerm;
    }
  },

  data: function() {

    return {
      item: {
        varName: this.filter.varName,
        searchTerm: this.filter.default.searchTerm,
        op: this.filter.default.op,
      },
      options: {
        searchTermCaption: null,
        changed: this.filter.options.changed,
      }
    }

  },

  watch: {
    // update prop 'filter' from store
    item: {
      handler: function(value){
        if (this.item.searchTerm !== this.filter.default.searchTerm) { // update when filter is not activated
          this.options.changed = true;
          this.$emit('change', this.item, true);
        } else {
          this.options.changed = false;
          this.$emit('change', this.item, false);
        }
      },
      deep: true,
    },

    // update prop 'filter' from store
    filter: {
      handler: function(){
        if (!this.filter.changed) { // update when filter is not activated
          this.item.searchTerm = this.filter.value.searchTerm;
        }
      },
      deep: true,
    }
  }
});
