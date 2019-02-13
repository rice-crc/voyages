template = `
  <div class="v-form-group">
    <div class="v-title">
      <span>{{filter.label}}</span>
      <b-badge pill
        v-if="filter.options.isImputed"
        v-b-tooltip.hover title="` +
          gettext('Imputed results are calculated by an algorithm.') +
        `" variant="secondary"
        class="v-badge-imputed">` +
          gettext('IMPUTED') +
      `</b-badge>
    </div>
    <div class="v-description" v-text="filter.description"></div>

    <div class="row">
      <div class="col-md-4">
        <v-select @changed="updateOp" :value="item.op"></v-select>
      </div>
      <div class="col-md-4" v-if="options.searchTerm1Disabled">
        <datepicker 
          :typeable=datepickerFromOptions.typeable 
          :format=datepickerFromOptions.format
          :disabledDates=datepickerFromOptions.disabledDates
          :bootstrapStyling=datepickerFromOptions.bootstrapStyling
          :initial-view=datepickerFromOptions.initialView
          :openDate=datepickerFromOptions.openDate
          :clearButton=datepickerFromOptions.clearButton
          :value=item.searchTerm0
          @selected="updateSearchTerm0"
          placeholder="">
        </datepicker>
      </div>
      <div class="col-md-8" v-if="!options.searchTerm1Disabled">
        <datepicker 
          :typeable=datepickerFromOptions.typeable 
          :format=datepickerFromOptions.format
          :disabledDates=datepickerFromOptions.disabledDates
          :bootstrapStyling=datepickerFromOptions.bootstrapStyling
          :initial-view=datepickerFromOptions.initialView
          :openDate=datepickerFromOptions.openDate
          :clearButton=datepickerFromOptions.clearButton
          :value=item.searchTerm0
          @selected="updateSearchTerm0"
          placeholder="">
        </datepicker>
      </div>
      <div class="col-md-4" v-if="options.searchTerm1Disabled">
        <datepicker 
          :typeable=datepickerToOptions.typeable 
          :format=datepickerToOptions.format
          :disabledDates=datepickerToOptions.disabledDates
          :bootstrapStyling=datepickerToOptions.bootstrapStyling
          :initial-view=datepickerToOptions.initialView
          :openDate=datepickerToOptions.openDate
          :clearButton=datepickerToOptions.clearButton
          :value=item.searchTerm1
          calendarClass="v-datepicker-cal-right"	
          @selected="updateSearchTerm1"
          placeholder="">
        </datepicker>
      </div>
    </div>

    <div class="row v-padding" v-if="false">
      <div class="col-md-12">
        <div>
          <code>{{item}}</code>
        </div>
        <div>
          <b-button :disabled="!options.changed" variant="success" size="sm" @click="apply">` +
          gettext('Apply') +
          `</b-button>
          <b-button :disabled="!options.changed" variant="secondary" size="sm" @click="reset">` +
          gettext('Reset') +
          `</b-button>
        </div>
      </div>
    </div>

  </div>

  `;


// v-datepicker
Vue.component("v-datepicker", {
  props: ['filter'],
  template: template,

  components: {
    datepicker: vuejsDatepicker,
  },

  data: function(){
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
        caption: this.filter.options.caption,
        changed: false,
      },
      datepickerFromOptions: {
        format: "yyyy/MM/dd",
        disabledDates: {
          // the months' indexes start with 0
          to: new Date(1514, 0, 1), // Disable all dates up to specific date
          from: new Date(1866, 11, 31) // Disable all dates after specific date
        },
        typeable: true,
        bootstrapStyling: true,
        initialView: "year",
        openDate: new Date(1514, 0, 1),
        clearButton: true,
      },
      datepickerToOptions: {
        format: "yyyy/MM/dd",
        disabledDates: {
          // the months' indexes start with 0
          to: new Date(1514, 0, 1), // Disable all dates up to specific date
          from: new Date(1866, 11, 31) // Disable all dates after specific date
        },
        typeable: true,
        bootstrapStyling: true,
        initialView: "year",
        openDate: new Date(1514, 0, 1),
        clearButton: true,
      },
    }
  },

  methods: {
    // form element handlers
    updateSearchTerm0(value) { // handler for variable
      // update the to datepicker
      this.datepickerToOptions.disabledDates.to = value;
      this.item.searchTerm0 = moment(value).format(SOLR_DATE_FORMAT);
    },
    updateSearchTerm1(value) { // handler for variable
      this.datepickerFromOptions.disabledDates.from = value;
      this.item.searchTerm1 = moment(value).format(SOLR_DATE_FORMAT);
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
      handler: function () {
        // set "" to null
        this.item.searchTerm0 = (this.item.searchTerm0 == "" | this.item.searchTerm0 == "Invalid date") ? null : this.item.searchTerm0;
        this.item.searchTerm1 = (this.item.searchTerm1 == "" | this.item.searchTerm0 == "Invalid date") ? null : this.item.searchTerm1;

        // labels
        if (this.item.op == "is between") {
          this.options.searchTerm1Disabled = true;
          this.options.searchTermCaption0 = gettext("Enter the lower bound");
          this.options.searchTermCaption1 = gettext("Enter the upper bound");
        } else {
          this.options.searchTerm1Disabled = false;
          this.item.searchTerm1 = null;
          if (this.item.op == "is at most") {
            this.options.searchTermCaption0 = gettext("Enter the upper bound");
          }
          if (this.item.op == "is at least") {
            this.options.searchTermCaption0 = gettext("Enter the lower bound");
          }
          if (this.item.op == "is equal to") {
            this.options.searchTermCaption0 = this.searchTermCaption;
          }
        }

        // control visibility
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
      handler: function(value){
        if (!this.filter.changed) { // update when filter is not activated
          this.item.searchTerm0 = this.filter.value.searchTerm0;
          this.item.searchTerm1 = this.filter.value.searchTerm1;
          this.item.op = this.filter.value.op;
        }
      },
      deep: true,
    }
  },

});