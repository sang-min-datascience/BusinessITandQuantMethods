--[[
sheet.lua: draws a small spreadsheet grid (column letters, row numbers) from a
code block with class "sheet".

Syntax (cells separated by "|", one line per row):

```{.sheet title="Price sheet" highlight="D2"}
Product      | Net price | VAT rate | VAT            | Gross price
Coffee 250 g | 6.50      | 19%      | =B2*C2 -> 1.24 | =B2+D2 -> 7.74
```

* A cell that starts with "=" is shown as a formula. Add " -> value" to show
  the value the formula returns underneath it.
* Options: title="..."  caption under the grid
           highlight="D2 E3"  cells to outline (space separated)
           start-row="5"  number of the first row (default 1)
           start-col="B"  letter of the first column (default A)
           header="false" first row is ordinary data, not bold labels
]]

local function esc(s)
  s = s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
  return s
end

local function trim(s) return (s:gsub("^%s+", ""):gsub("%s+$", "")) end

local function col_letter(n) -- 1 -> A
  local s = ""
  while n > 0 do
    local r = (n - 1) % 26
    s = string.char(65 + r) .. s
    n = (n - 1 - r) // 26
  end
  return s
end

local function col_number(letters)
  local n = 0
  for i = 1, #letters do n = n * 26 + (letters:byte(i) - 64) end
  return n
end

local function split_row(line)
  local cells = {}
  for cell in (line .. "|"):gmatch("(.-)|") do table.insert(cells, trim(cell)) end
  return cells
end

function CodeBlock(el)
  if not el.classes:includes("sheet") then return nil end
  if not quarto.doc.is_format("html") then
    return pandoc.CodeBlock(el.text) -- plain fallback for other formats
  end

  local start_row = tonumber(el.attributes["start-row"] or "1")
  local start_col = col_number((el.attributes["start-col"] or "A"):upper())
  local has_header = (el.attributes["header"] or "true") ~= "false"
  local highlight = {}
  for ref in (el.attributes["highlight"] or ""):gmatch("%S+") do highlight[ref:upper()] = true end

  local rows, ncol = {}, 0
  for line in el.text:gmatch("[^\n]+") do
    if trim(line) ~= "" then
      local cells = split_row(line)
      ncol = math.max(ncol, #cells)
      table.insert(rows, cells)
    end
  end

  local h = {}
  table.insert(h, '<figure class="sheet-figure"><div class="sheet-scroll"><table class="sheet">')
  table.insert(h, '<thead><tr><th class="sheet-corner"></th>')
  for c = 0, ncol - 1 do
    table.insert(h, '<th class="sheet-col">' .. col_letter(start_col + c) .. '</th>')
  end
  table.insert(h, '</tr></thead><tbody>')
  for r, cells in ipairs(rows) do
    local rownum = start_row + r - 1
    table.insert(h, '<tr><th class="sheet-row">' .. rownum .. '</th>')
    for c = 1, ncol do
      local raw = cells[c] or ""
      local ref = col_letter(start_col + c - 1) .. rownum
      local classes = {}
      if r == 1 and has_header then table.insert(classes, "sheet-label") end
      if highlight[ref] then table.insert(classes, "sheet-active") end
      local inner
      if raw:sub(1, 1) == "=" then
        table.insert(classes, "sheet-formula")
        local f, v = raw:match("^(.-)%s*%->%s*(.+)$")
        if not f then f = raw end
        inner = '<code>' .. esc(f) .. '</code>'
        if v then inner = inner .. '<span class="sheet-value">' .. esc(v) .. '</span>' end
      else
        if raw:match("^[%d%.,%-%%€$£]+$") then table.insert(classes, "sheet-num") end
        inner = esc(raw)
      end
      table.insert(h, '<td class="' .. table.concat(classes, " ") .. '" title="' .. ref .. '">' .. inner .. '</td>')
    end
    table.insert(h, '</tr>')
  end
  table.insert(h, '</tbody></table></div>')
  local title = el.attributes["title"]
  table.insert(h, '<figcaption class="sheet-caption"><span class="sheet-badge">Spreadsheet</span>')
  if title then table.insert(h, ' ' .. esc(title)) end
  table.insert(h, '</figcaption></figure>')
  return pandoc.RawBlock("html", table.concat(h))
end
