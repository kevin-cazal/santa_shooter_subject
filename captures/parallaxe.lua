-- title: santa
-- script: lua

W=240
H=136
player_x=116
player_y=64
player_speed=1.5
bullet_x=-10
bullet_y=-10
bullet_speed=0
enemy_x=W+20
enemy_y=60
enemy_speed=-1.2
score=0
function check_collision(ax, ay, aw, ah, bx, by, bw, bh)
	return ax <= bx + bw and ax + aw >= bx and ay <= by + bh and ay + ah >= by
end
stars = {}
for i=1,50 do local size = math.random(1,3) table.insert(stars, {x=math.random(0,W), y=math.random(0,H), size=size, speed=size*0.3}) end
function TIC()
	for i,s in ipairs(stars) do s.x = s.x - s.speed if s.x < 0 then s.x = W end end
	cls(0)
	for i,s in ipairs(stars) do circ(s.x, s.y, s.size - 1, 12) end
	spr(0, player_x, player_y, 0, 1, 0, 0, 2)
end

-- <TILES>
-- 000:c0000000c2000000c2220000c22222ccc22222ccc2220000c2000000c0000000
-- 001:00000000000000000000000ccccccccccccccccc0000000c0000000000000000
-- 002:ccccceee8888cceeaaaa0cee888a0ceeccca0ccc0cca0c0c0cca0c0c0cca0c0c
-- 003:eccccccccc888888caaaaaaaca888888cacccccccacccccccacc0ccccacc0ccc
-- 004:ccccceee8888cceeaaaa0cee888a0ceeccca0cccccca0c0c0cca0c0c0cca0c0c
-- 016:0055550005555550555555555525525555555555550000550505505000555500
-- 017:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
-- 018:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
-- 019:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
-- 020:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
-- </TILES>

-- <WAVES>
-- 000:00000000ffffffff00000000ffffffff
-- 001:0123456789abcdeffedcba9876543210
-- 002:0123456789abcdef0123456789abcdef
-- </WAVES>

-- <SFX>
-- 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
-- </SFX>

-- <TRACKS>
-- 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
-- </TRACKS>

-- <PALETTE>
-- 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
-- </PALETTE>

