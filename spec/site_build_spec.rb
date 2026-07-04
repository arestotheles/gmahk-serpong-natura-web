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

  it "builds key pages" do
    %w[berita/index.html acara/index.html kontak/index.html tentang-kami/index.html].each do |path|
      expect(File).to exist(File.join(site_dir, path)), "missing #{path}"
    end
  end

  it "includes all navigation labels on home" do
    html = File.read(File.join(site_dir, "index.html"))
    expect(html).to include("Tentang Kami")
    expect(html).to include("Jadwal Ibadah")
    expect(html).to include("Berita")
    expect(html).to include("Kontak")
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

  it "includes contact map embed" do
    html = File.read(File.join(site_dir, "kontak", "index.html"))
    expect(html).to include("<iframe")
    expect(html).to include("maps.google.com")
  end
end
