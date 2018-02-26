Vue.component('v-number', {
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
        <div class="col-md-4">
          <v-select @changed="updateOp" :value="item.op"></v-select>
        </div>
        <div class="col-md-4" v-if="options.searchTerm1Disabled">
          <v-textbox @entered="updateSearchTerm0" :search-term-caption="options.searchTermCaption0" :value="item.searchTerm0" :type="filter.type"></v-textbox>
        </div>
        <div class="col-md-8" v-if="!options.searchTerm1Disabled">
          <v-textbox @entered="updateSearchTerm0" :search-term-caption="options.searchTermCaption0" :value="item.searchTerm0" :type="filter.type"></v-textbox>
        </div>
        <div class="col-md-4" v-if="options.searchTerm1Disabled">
          <v-textbox @entered="updateSearchTerm1" :search-term-caption="options.searchTermCaption1" :value="item.searchTerm1" :type="filter.type"></v-textbox>
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
        searchTerm0: this.filter.default.searchTerm0,
        searchTerm1: this.filter.default.searchTerm1,
        op: this.filter.default.op,
      },
      options: {
        searchTerm1Disabled: false,
        searchTermCaption0: null,
        searchTermCaption1: null,
        changed: false,
      }
    }
  },

  methods: {
    // form element handlers
    updateSearchTerm0(value) { // handler for variable
      this.item.searchTerm0 = value;
    },
    updateSearchTerm1(value) { // handler for variable
      this.item.searchTerm1 = value;
    },
    updateOp(value) { // handler for variable
      this.item.op = value;
    },

    // form action buttons
    apply() { // simply return the search string to whichever requested for it
      var searchString = JSON.stringify(this.item);
      alert(searchString);
    },

    reset() { // reset data; observers will take care of resetting the controls
      this.item.searchTerm0 = this.filter.default.searchTerm0;
      this.item.searchTerm1 = this.filter.default.searchTerm1;
      this.item.op = this.filter.default.op;
    }
  },

  watch: {
    // search object
    item: {
      handler: function(){
        // set "" to null
        this.item.searchTerm0 = (this.item.searchTerm0 == "") ? null:this.item.searchTerm0;
        this.item.searchTerm1 = (this.item.searchTerm1 == "") ? null:this.item.searchTerm1;

        // convert to number
        if (this.item.searchTerm0) this.item.searchTerm0 = parseInt(this.item.searchTerm0);
        if (this.item.searchTerm1) this.item.searchTerm1 = parseInt(this.item.searchTerm1);

        // labels
        if (this.item.op == "between") {
          this.options.searchTerm1Disabled = true;
          this.options.searchTermCaption0 = "Enter the lower bound";
          this.options.searchTermCaption1 = "Enter the upper bound";
        } else {
          this.options.searchTerm1Disabled = false;
          this.item.searchTerm1 = null;
          if (this.item.op == "is less than") {
            this.options.searchTermCaption0 = "Enter the upper bound";
          }
          if (this.item.op == "is more than") {
            this.options.searchTermCaption0 = "Enter the lower bound";
          }
          if (this.item.op == "equals to") {
            this.options.searchTermCaption0 = this.searchTermCaption;
          }
        }

        // control visibility
        debugger;
        if (this.item.searchTerm0 !== null || this.item.searchTerm1 !== null) {
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
          this.item.searchTerm0 = this.filter.value.searchTerm0;
          this.item.searchTerm1 = this.filter.value.searchTerm1;
          this.item.op = this.filter.value.op;
        }
      },
      deep: true,
    }
  },
  created: function(){
    // labels
    if (this.item.op == "between") {
      this.options.searchTerm1Disabled = true;
      this.options.searchTermCaption0 = "Enter the lower bound";
      this.options.searchTermCaption1 = "Enter the upper bound";
    } else {
      this.options.searchTerm1Disabled = false;
      this.item.searchTerm1 = null;
      if (this.item.op == "is less than") {
        this.options.searchTermCaption0 = "Enter the upper bound";
      }
      if (this.item.op == "is more than") {
        this.options.searchTermCaption0 = "Enter the lower bound";
      }
      if (this.item.op == "equals to") {
        this.options.searchTermCaption0 = this.searchTermCaption;
      }
    }
  }

})
// end of input
