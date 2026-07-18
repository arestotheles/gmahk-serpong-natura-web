# frozen_string_literal: true

require "spec_helper"

RSpec.describe "Site build" do
  before(:all) do
    system("bundle exec jekyll build", chdir: File.expand_path("..", __dir__), exception: true)
  end

  let(:site_dir) { File.expand_path("../_site", __dir__) }

  it "builds index.html" do
    expect(File).to exist(File.join(site_dir, "index.html"))
  end

  it "builds archive pages and redirect stubs" do
    %w[berita/index.html acara/index.html tentang-kami/index.html jadwal-ibadah/index.html kontak/index.html].each do |path|
      expect(File).to exist(File.join(site_dir, path)), "missing #{path}"
    end
  end

  it "orders home sections hero through kontak" do
    html = File.read(File.join(site_dir, "index.html"))
    ids = %w[hero jadwal tentang acara berita kontak]
    positions = ids.map { |id| html.index("id=\"#{id}\"") }
    expect(positions).to all(be_a(Integer))
    expect(positions).to eq(positions.sort)
  end

  it "includes navigation labels on home" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html).to include("Tentang Kami")
    expect(html).to include("Jadwal Ibadah")
    expect(html).to include("Berita")
    expect(html).to include("Kontak")
  end

  it "uses anchor links in navigation" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html).to include("#jadwal")
    expect(html).to include("#tentang")
    expect(html).to include("#kontak")
  end

  it "includes mobile viewport meta tag" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html).to include('name="viewport"')
  end

  it "shows at most two berita previews on home (AE2)" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html.scan("berita-card").length).to eq(2)
    expect(html).to include("Lihat semua")
  end

  it "includes contact map on home" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html).to include("<iframe")
    expect(html).to include("maps.google.com")
    expect(html).not_to include("<form")
  end

  it "redirects legacy tentang-kami URL" do
    html = File.read(File.join(site_dir, "tentang-kami", "index.html"))
    expect(html).to include("http-equiv=\"refresh\"")
    expect(html).to include("#tentang")
  end

  it "renders mixed-storage berita post (AE1)" do
    berita_files = Dir.glob(File.join(site_dir, "berita", "**", "index.html"))
    post_html = berita_files.map { |f| File.read(f) }.find { |h| h.include?("cloudfront.net") }
    expect(post_html).not_to be_nil
    expect(post_html).to include("cloudfront.net/berita/cover-pengumuman.jpg")
    expect(post_html).to include("sample-buletin.pdf")
  end

  it "keeps events off berita archive (AE3)" do
    berita_html = File.read(File.join(site_dir, "berita", "index.html"))
    expect(berita_html).not_to include("Perkemahan Pemuda")
    acara_html = File.read(File.join(site_dir, "acara", "index.html"))
    expect(acara_html).to include("Perkemahan Pemuda")
  end

  it "hides Instagram berita when sync is disabled (AE4)" do
    berita_html = File.read(File.join(site_dir, "berita", "index.html"))
    home_html = File.read(File.join(site_dir, "index.html"))
    expect(berita_html).not_to include("[Fixture] Instagram Berita Tersembunyi")
    expect(home_html).not_to include("[Fixture] Instagram Berita Tersembunyi")
  end

  describe "Instagram berita when enabled" do
    before(:all) do
      @repo_root = File.expand_path("..", __dir__)
      @instagram_config_path = File.join(@repo_root, "_data", "instagram.yml")
      @original_instagram_config = File.read(@instagram_config_path)
      enabled_config = @original_instagram_config.gsub("enabled: false", "enabled: true")
      File.write(@instagram_config_path, enabled_config)
      system("bundle exec jekyll build", chdir: @repo_root, exception: true)
      @enabled_site_dir = File.join(@repo_root, "_site")
    end

    after(:all) do
      File.write(@instagram_config_path, @original_instagram_config)
    end

    it "shows Dari Instagram badge on enabled fixture post (AE3)" do
      post_html = File.read(File.join(@enabled_site_dir, "berita", "2026", "05", "15", "ig-fixture-hidden", "index.html"))
      expect(post_html).to include("Dari Instagram")
      expect(post_html).to include("https://cdninstagram.com/fixture/hidden.jpg")
    end

    it "lists enabled Instagram berita on archive page" do
      berita_html = File.read(File.join(@enabled_site_dir, "berita", "index.html"))
      expect(berita_html).to include("[Fixture] Instagram Berita Tersembunyi")
    end
  end

  it "points berita archive nav to home anchor" do
    html = File.read(File.join(site_dir, "berita", "index.html"))
    expect(html).to include("#berita")
  end
end
