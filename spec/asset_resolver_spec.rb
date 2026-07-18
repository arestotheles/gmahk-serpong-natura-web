# frozen_string_literal: true

require "spec_helper"

RSpec.describe AssetResolver do
  describe ".resolve" do
    it "resolves github storage with baseurl" do
      asset = { "storage" => "github", "path" => "assets/images/foo.jpg" }
      expect(described_class.resolve(asset, baseurl: "/gmahk-serpong-natura-web")).to eq(
        "/gmahk-serpong-natura-web/assets/images/foo.jpg"
      )
    end

    it "resolves s3 storage with external url unchanged" do
      asset = { "storage" => "s3", "url" => "https://d123.cloudfront.net/foo.jpg" }
      expect(described_class.resolve(asset, baseurl: "/base")).to eq("https://d123.cloudfront.net/foo.jpg")
    end

    it "resolves external storage with https url unchanged" do
      asset = { "storage" => "external", "url" => "https://cdninstagram.com/v/image.jpg" }
      expect(described_class.resolve(asset, baseurl: "/base")).to eq("https://cdninstagram.com/v/image.jpg")
    end

    it "raises when external storage uses non-https url" do
      asset = { "storage" => "external", "url" => "http://cdninstagram.com/v/image.jpg" }
      expect { described_class.resolve(asset, baseurl: "") }.to raise_error(ArgumentError, /https URL/)
    end

    it "raises when external storage lacks url" do
      asset = { "storage" => "external" }
      expect { described_class.resolve(asset, baseurl: "") }.to raise_error(ArgumentError, /requires 'url'/)
    end

    it "raises when github storage lacks path" do
      asset = { "storage" => "github" }
      expect { described_class.resolve(asset, baseurl: "") }.to raise_error(ArgumentError, /requires 'path'/)
    end

    it "raises when s3 storage lacks url" do
      asset = { "storage" => "s3" }
      expect { described_class.resolve(asset, baseurl: "") }.to raise_error(ArgumentError, /requires 'url'/)
    end

    it "raises for unknown storage type" do
      asset = { "storage" => "dropbox", "path" => "x" }
      expect { described_class.resolve(asset, baseurl: "") }.to raise_error(ArgumentError, /Unknown storage type/)
    end
  end

  describe ".resolve_cover" do
    it "returns nil when cover is nil" do
      expect(described_class.resolve_cover(nil, baseurl: "")).to be_nil
    end
  end
end
