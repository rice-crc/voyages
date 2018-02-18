// v-panel
Vue.component('v-panel', {
  props: ['title', "isAdvanced", "filters", "count", "group", "subGroup"],
  template: `
    <li v-if="isAdvancedValue" class="dropdown-item dropdown-item-li search-dropdown-item" :data-submenu-id="idValue">
        <div class="dropdown-menu-title">
          <div class="dropdown-menu-title-text">
            {{titleValue}}
          </div>
          <div class="dropdown-menu-title-count">
            <b-badge variant="danger" v-if="count">{{count}}</b-badge>
          </div>
        </div>
        <div :id="idValue" class="search-submenu popover">
            <div class="popover-content">
              <slot name="v-panel-header"></slot>
              <slot name="v-panel-content" :filters="filtersValue"></slot>
              <div class="margin-v">
                <b-button :disabled="controlDisabled" variant="info" size="sm" @click="apply">
                  Apply
                </b-button>
                <b-button :disabled="controlDisabled" variant="outline-secondary" size="sm" @click="reset">
                  Reset
                </b-button>
              </div>
            </div>
        </div>
    </li>
  `,

  data: function() {
    return {
      titleValue: '',
      isAdvancedValue: '',
      idValue: null,
      filtersValue: null,
      controlDisabled: true,
    }
  },

  methods: {
    apply() {
      this.$emit('apply', this.group, this.filtersValue);
    },
    reset(group, subGroup) {
      this.$emit('reset', this.group, this.subGroup);
    }
  },

  watch: {
    count: {
      handler: function(){
        this.controlDisabled = (this.count.changed > 0) ? false:true;
      },
      deep: true,
    }
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.isAdvancedValue = this.isAdvanced;
    this.idValue = hyphenate(this.title);
    this.filtersValue = this.filters;
  }

})
// v-panel

// v-panel-header
Vue.component('v-panel-header', {
  props: ['title', "description", "count"],
  template: `
    <div class="v-panel-header">
      <div class="v-panel-title-container">
        <div class="v-panel-title">
        {{title}}
        </div>
        <div class="v-panel-counter">
          <div class="text-center">
          <!--
            <b-button variant="info" size="sm">
              Parameters Applied <b-badge variant="light">{{count}}</b-badge>
            </b-button>
          -->

          <b-btn variant="outline-info" size="sm" v-b-modal.modal-center>
            <i class="fa fa-question-circle-o"></i>
            Help
          </b-btn>
          <b-modal id="modal-center" centered title="modalTitle">
            <slot name="v-modal-content"></slot>
          </b-modal>

          </div>
        </div>
      </div>
      <div class="v-panel-description" v-text="description"></div>

    </div>
  `,

  data: function() {
    return {
      titleValue: '',
      descriptionValue: '',
      countValue: null,
      modalTitle: '',
    }
  },

  methods: {
    emitParent: function() {
      this.$emit('blurred', this.textboxValue);
    }
  },

  watch: {
    title: { // this is the value from props
      handler: function(value) {
        this.titleValue = value; // titleValue is the local copy used in the child component
      }
    },
    description: {
      handler: function(value) {
        this.descriptionValue = value; // descriptionValue is the local copy used in the child component
      }
    },
    count: {
      handler: function(value) {
        this.countValue = value; // countValue is the local copy used in the child component
      }
    },
    filters: {

    }


  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.descriptionValue = this.description;
    this.countValue = this.count;
    this.modalTitle = "Help about " + this.title;
  }

})
// v-panel-header
