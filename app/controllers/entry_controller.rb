class EntryController < ApplicationController
	before_action :set_entry, only: [:update]
    def update    	
    	puts "sfd"
    	@entry.update(entry_params)
  	end

  	private
	    # Use callbacks to share common setup or constraints between actions.
	    def set_entry
	      @entry = Entry.find(params[:guid])
	    end

	    # Never trust parameters from the scary internet, only allow the white list through.
	    def entry_params
	      params.permit(:guid, :click_bait)
	    end
end
