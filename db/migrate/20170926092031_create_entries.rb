class CreateEntries < ActiveRecord::Migration
  def change
    create_table :entries, id: false, force: true do |t|
      t.string :guid, null: false
      t.string :source
      t.string :url
      t.string :title
      t.string :summary
      t.datetime :published
      t.boolean :click_bait
      t.integer :cluster

      t.timestamps null: false
    end

    add_index :entries, :guid, unique: true

  end
end
