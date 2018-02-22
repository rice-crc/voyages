// v-panel-header
Vue.component('v-panel-header', {
  props: ['title', "description", "modalDisabled"],
  template: `
    <div class="v-panel-header">
      <div class="v-panel-title-container">
        <div class="v-panel-title">
          {{title}}
        </div>
        <div v-if="!modalDisabled" class="v-panel-header-control" >
          <div class="text-center">
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
      modalTitle: '',
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
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.descriptionValue = this.description;
    this.modalTitle = "Help about " + this.title;
  }

})
// v-panel-header
