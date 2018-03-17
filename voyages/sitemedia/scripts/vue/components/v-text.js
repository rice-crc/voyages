Vue.component('v-text', {
  props: ['filter'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{filter.label}}</span>
        <span>
          <b-badge
            v-if="filter.options.isImputed"
            v-b-tooltip.hover title="Imputed variables are calculated by an algorithm and not based on historical records."
            variant="warning"
            class="v-badge-imputed">
            Imputed
          </b-badge>
          <b-badge
            v-if="filter.options.isAdvanced"
            v-b-tooltip.hover title="Advanced variables are additional parameters that are frequenlty used. They do not change current search behavior."
            variant="danger" class="v-badge-advanced">Advanced</b-badge>
        </span>
      </div>
      <div class="v-description" v-text="filter.description"></div>

      <div class="row">
        <div class="col-md-12">
          <v-textbox @entered="updateSearchTerm" :search-term-caption="options.searchTermCaption" :value="item.searchTerm"></v-textbox>
        </div>
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

  methods: {
    // form element handlers
    updateSearchTerm(value) { // handler for variable
      this.item.searchTerm = value;
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

  watch: {
    // search object
    item: {
      handler: function(){
        // set "" to null
        this.item.searchTerm = (this.item.searchTerm == "") ? null:this.item.searchTerm;

        // control visibility
        if (this.item.searchTerm !== null) {
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
  },

})
// end of input
