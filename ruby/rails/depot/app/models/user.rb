class User < ActiveRecord::Base
  validates_presence_of :name
  validates_uniqueness_of :name

  attr_accessor :password_confirmation
  validates_confirmation_of :password
  validate :password_non_blank

  private
  def password_non_blank
    errors.add(:password, "Missing password") if hashed_password.blank?
  end

  def self.encrypted_password(password, salt)
    string_to_hash = password + "wibble" + salt
    Digest::SHA1.hexdigest(string_to_hash)
  end

  def create_new_salt
    self.salt = self.object_id.to_s + rand.to_s
  end
end
