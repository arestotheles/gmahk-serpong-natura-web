# frozen_string_literal: true

module AssetResolver
  STORAGE_TYPES = %w[github s3 external].freeze

  def self.resolve(asset, baseurl: "")
    raise ArgumentError, "Asset is required" if asset.nil? || asset.empty?

    storage = asset["storage"] || asset[:storage]
    raise ArgumentError, "Unknown storage type '#{storage}'. Use 'github', 's3', or 'external'." unless STORAGE_TYPES.include?(storage)

    case storage
    when "github"
      path = asset["path"] || asset[:path]
      raise ArgumentError, "storage: github requires 'path'" if path.nil? || path.to_s.strip.empty?

      normalized = path.to_s.delete_prefix("/")
      "#{baseurl}/#{normalized}"
    when "s3", "external"
      url = asset["url"] || asset[:url]
      raise ArgumentError, "storage: #{storage} requires 'url'" if url.nil? || url.to_s.strip.empty?

      url = url.to_s
      raise ArgumentError, "storage: external requires an https URL" if storage == "external" && !url.start_with?("https://")

      url
    end
  end

  def self.resolve_cover(cover, baseurl: "")
    return nil if cover.nil? || cover.empty?

    resolve(cover, baseurl: baseurl)
  end
end

Liquid::Template.register_filter(Module.new do
  def resolve_asset(asset)
    AssetResolver.resolve(asset, baseurl: @context.registers[:site].baseurl)
  end

  def resolve_cover(cover)
    AssetResolver.resolve_cover(cover, baseurl: @context.registers[:site].baseurl)
  end
end)
