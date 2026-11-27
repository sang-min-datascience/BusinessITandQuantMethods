--[[
panopto.lua: embeds a Panopto video, or shows a placeholder until it exists.

Use a div with class "video":

::: {.video panopto="1a2b3c4d-...-session id" minutes="10"}
Percentages and percent change
:::

The text inside the div is the video's title. Without a panopto id the
filter shows a "video coming soon" box, so chapters can be written before
the recordings exist. The server name comes from `panopto-host` in
_quarto.yml.
]]

local host = nil

function Meta(meta)
  if meta["panopto-host"] then host = pandoc.utils.stringify(meta["panopto-host"]) end
end

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

function Div(el)
  if not el.classes:includes("video") then return nil end
  if not quarto.doc.is_format("html") then return el.content end
  local title = pandoc.utils.stringify(el.content)
  local id = el.attributes["panopto"]
  local minutes = el.attributes["minutes"]
  local meta = minutes and (' · about ' .. esc(minutes) .. ' min') or ''
  local html
  if id and id ~= "" and host and not host:match("YOUR%-") then
    local src = "https://" .. host .. "/Panopto/Pages/Embed.aspx?id=" .. id ..
      "&autoplay=false&offerviewer=true&showtitle=false&showbrand=false&interactivity=none"
    html = '<figure class="video-box"><div class="video-frame"><iframe src="' .. src ..
      '" title="' .. esc(title) .. '" allowfullscreen allow="autoplay; fullscreen" loading="lazy"></iframe></div>' ..
      '<figcaption><span class="video-badge">Video</span> ' .. esc(title) .. meta .. '</figcaption></figure>'
  else
    html = '<figure class="video-box video-pending"><div class="video-frame video-placeholder">' ..
      '<span class="video-icon">▶</span><span>Video coming soon</span></div>' ..
      '<figcaption><span class="video-badge">Video</span> ' .. esc(title) .. meta .. '</figcaption></figure>'
  end
  return pandoc.RawBlock("html", html)
end

return { { Meta = Meta }, { Div = Div } }
