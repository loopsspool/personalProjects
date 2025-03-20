// RESOLUTION SETTINGS
$fa = 1;
$fs = 0.4;

wheel_radius = 6;
base_height = 6;
base_top = 8;
wheel_track = 13;
wheel_width = 6;
wheel_rotation = 40;

// CAR BODY
scale([1.2, 1, 1.2])
{
	rotate([wheel_rotation/3, 0, 0])
	{
		// BASE
		cube([60, 20, base_height], center = true);
		// TOP
		translate([5, 0, (base_height/2 + base_top/2) 	- 0.01])
			cube([30, 20, base_top], center = true);
	}

// WHEELS
// FRONT LEFT
translate([-20, -wheel_track, 0])
	rotate([90, 0, wheel_rotation])
		cylinder(h = wheel_width, r = wheel_radius, center = true);
// FRONT RIGHT
translate([-20, wheel_track, 0])
	rotate([90, 0, wheel_rotation])
		cylinder(h = wheel_width, r = wheel_radius, center = true);

// REAR RIGHT
translate([20, wheel_track, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_width, r = wheel_radius, center = true);
// REAR LEFT
translate([20, -wheel_track, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_width, r = wheel_radius, center = true);

// AXLES
// FRONT
translate([-20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_track * 2, r = 2, center = true);
// REAR
translate([20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_track * 2, r = 2, center = true);
}