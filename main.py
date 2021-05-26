from xml.dom import minidom


radius = 0.025
length = 0.07
boxSize = "0.1 0.1 0.1"


def createBlackMaterial():
    root = minidom.Document()

    material = root.createElement('material')
    color = root.createElement('color')
    material.setAttribute('name', 'Black')
    color.setAttribute('rgba', '0.2 0.2 0.2 1.0')
    material.appendChild(color)

    return material


def createWhiteMaterial():
    root = minidom.Document()

    material = root.createElement('material')
    color = root.createElement('color')
    material.setAttribute('name', 'White')
    color.setAttribute('rgba', '1.0 1.0 1.0 1.0')
    material.appendChild(color)

    return material


def createOrigin(xyz, rpy=None):
    root = minidom.Document()

    origin = root.createElement('origin')
    origin.setAttribute('xyz', xyz)

    if rpy is not None:
        origin.setAttribute('rpy', rpy)

    return origin


def createBoxGeometry(size):
    root = minidom.Document()

    geometry = root.createElement('geometry')
    box = root.createElement('box')
    box.setAttribute('size', size)

    geometry.appendChild(box)

    return geometry


def createCylinderGeometry(radius, length):
    root = minidom.Document()

    geometry = root.createElement('geometry')
    cylinder = root.createElement('cylinder')
    cylinder.setAttribute('length', str(length))
    cylinder.setAttribute('radius', str(radius))

    geometry.appendChild(cylinder)

    return geometry


def createMeshGeometry(filename):
    root = minidom.Document()

    geometry = root.createElement('geometry')
    mesh = root.createElement('mesh')
    mesh.setAttribute('filename', filename)

    geometry.appendChild(mesh)

    return geometry


def createSphereGeometry(radius):
    root = minidom.Document()

    geometry = root.createElement('geometry')
    sphere = root.createElement('sphere')
    sphere.setAttribute('radius', str(radius))

    geometry.appendChild(sphere)

    return geometry


def createLink(name, material, geometry, origin=None):
    root = minidom.Document()

    link = root.createElement('link')
    visual = root.createElement('visual')

    link.setAttribute('name', name)

    link.appendChild(visual)
    visual.appendChild(geometry)
    visual.appendChild(material)

    if origin is not None:
        visual.appendChild(origin)

    return link


def createFixedJoint(name, parent_name, child_name, origin):
    root = minidom.Document()

    joint = root.createElement('joint')
    parent = root.createElement('parent')
    child = root.createElement('child')

    joint.setAttribute('name', name)
    joint.setAttribute('type', 'fixed')
    parent.setAttribute('link', parent_name)
    child.setAttribute('link', child_name)

    joint.appendChild(origin)
    joint.appendChild(parent)
    joint.appendChild(child)

    return joint


def createRevoluteJoint(name, parent_name, child_name, origin, axis_xyz):
    root = minidom.Document()

    joint = root.createElement('joint')
    axis = root.createElement('axis')
    parent = root.createElement('parent')
    child = root.createElement('child')

    joint.setAttribute('name', name)
    joint.setAttribute('type', 'revolute')
    axis.setAttribute('xyz', axis_xyz)
    parent.setAttribute('link', parent_name)
    child.setAttribute('link', child_name)

    joint.appendChild(axis)
    joint.appendChild(origin)
    joint.appendChild(parent)
    joint.appendChild(child)

    return joint


root = minidom.Document()
xml = root.createElement('robot')
xml.setAttribute('name', 'Kibo-chan')


xml.appendChild(createLink('base_link', createBlackMaterial(
), createBoxGeometry("0.01 0.01 0.01"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('base_rotation_link', createBlackMaterial(
), createBoxGeometry("0.1 0.1 0.07"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('torso_link', createWhiteMaterial(
), createCylinderGeometry(0.05, 0.20), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createRevoluteJoint('torso_joint', 'base_rotation_link',
                'torso_link', createOrigin("0 0 0.10", "0 0 0"), "0 0 1"))
xml.appendChild(createFixedJoint('base_rotation_joint', 'base_link',
                'base_rotation_link', createOrigin("0 0 0", "0 0 0")))

# 頭
xml.appendChild(createLink('neck_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('head_link', createBlackMaterial(
), createBoxGeometry("0.1 0.1 0.1"), createOrigin("0 0 0.05", "0 0 0")))
xml.appendChild(createRevoluteJoint('neck_link_joint', 'torso_link',
                'neck_link', createOrigin("0 0 0.12", "0 0 0"), "0 1 0"))
xml.appendChild(createRevoluteJoint('neck_head_joint', 'neck_link',
                'head_link', createOrigin("0 0 0", "0 0 0"), "1 0 0"))


# ここから左側
xml.appendChild(createLink('left_shoulder_link', createBlackMaterial(
), createBoxGeometry("0.025 0.015 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_shoulder_forward_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 0.02 0", "0 0 0")))
xml.appendChild(createLink('left_shoulder_up_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_upper_arm_link', createWhiteMaterial(
), createCylinderGeometry(0.0075, 0.1), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_elbow_link', createBlackMaterial(
), createBoxGeometry("0.035 0.035 0.05"), createOrigin("0 0 0", "0 0 1.57")))
xml.appendChild(createLink('left_wrist_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 0 -0.025", "1.57 0 0")))
xml.appendChild(createLink('left_lower_arm_link', createWhiteMaterial(
), createCylinderGeometry(0.0075, 0.1), createOrigin("0 0 0", "0 0 0")))

xml.appendChild(createLink('left_leg_up_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_leg_lap_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.2), createOrigin("0 0 -0.1", "0 0 0")))
xml.appendChild(createLink('left_leg_knee_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_leg_shank_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.2), createOrigin("0 0 -0.1", "0 0 0")))
xml.appendChild(createLink('left_leg_foot_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('left_leg_instep_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.1), createOrigin("0.05 0 -0.02", "0 1.57 0")))


xml.appendChild(createFixedJoint('left_shoulder_joint', 'torso_link',
                'left_shoulder_link', createOrigin("0 0.02 0.07", "0 0 0")))
xml.appendChild(createRevoluteJoint('left_upper_arm_joint', 'left_shoulder_up_link',
                'left_upper_arm_link', createOrigin("0 0 -0.05", "0 0 0"), "0 0 1"))
xml.appendChild(createRevoluteJoint('left_lower_arm_joint', 'left_elbow_link',
                'left_lower_arm_link', createOrigin("0 0 -0.05", "0 0 0"), "0 0 1"))
xml.appendChild(createRevoluteJoint('left_shoulder_forward_joint', 'left_shoulder_link',
                'left_shoulder_forward_link', createOrigin("0 0.025 0", "0 0 0"), "1 0 0"))
xml.appendChild(createRevoluteJoint('left_shoulder_up_joint', 'left_shoulder_forward_link',
                'left_shoulder_up_link', createOrigin("0 0.04 -0.01", "0 0 0"), "0 1 0"))
xml.appendChild(createRevoluteJoint('left_elbow_joint', 'left_upper_arm_link',
                'left_elbow_link', createOrigin("0 0 -0.05", "0 0 0"), "0 1 0"))
xml.appendChild(createRevoluteJoint('left_wrist_joint', 'left_lower_arm_link',
                'left_wrist_link', createOrigin("0 0 -0.05", "0 0 0"), "1 0 0"))

# 脚
xml.appendChild(createRevoluteJoint('left_leg_up_joint', 'base_rotation_link',
                'left_leg_up_link', createOrigin("0 0.05 -0.05", "0 0 0"), "1 0 0"))
xml.appendChild(createRevoluteJoint('left_leg_lap_joint', 'left_leg_up_link',
                'left_leg_lap_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))
xml.appendChild(createFixedJoint('left_leg_knee_joint', 'left_leg_lap_link',
                'left_leg_knee_link', createOrigin("0 0 -0.2", "0 0 0")))
xml.appendChild(createRevoluteJoint('left_leg_shank_joint', 'left_leg_knee_link',
                'left_leg_shank_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))
xml.appendChild(createFixedJoint('left_leg_foot_joint', 'left_leg_shank_link',
                'left_leg_foot_link', createOrigin("0 0 -0.2", "0 0 0")))
xml.appendChild(createRevoluteJoint('left_leg_instep_joint', 'left_leg_foot_link',
                'left_leg_instep_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))

# ここから右側
xml.appendChild(createLink('right_shoulder_link', createBlackMaterial(
), createBoxGeometry("0.025 0.015 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_shoulder_forward_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 -0.02 0", "0 0 0")))
xml.appendChild(createLink('right_shoulder_up_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_upper_arm_link', createWhiteMaterial(
), createCylinderGeometry(0.0075, 0.1), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_elbow_link', createBlackMaterial(
), createBoxGeometry("0.035 0.035 0.05"), createOrigin("0 0 0", "0 0 1.57")))
xml.appendChild(createLink('right_wrist_link', createBlackMaterial(
), createBoxGeometry("0.03 0.05 0.03"), createOrigin("0 0 -0.025", "1.57 0 0")))
xml.appendChild(createLink('right_lower_arm_link', createWhiteMaterial(
), createCylinderGeometry(0.0075, 0.1), createOrigin("0 0 0", "0 0 0")))

xml.appendChild(createLink('right_leg_up_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_leg_lap_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.2), createOrigin("0 0 -0.1", "0 0 0")))
xml.appendChild(createLink('right_leg_knee_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_leg_shank_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.2), createOrigin("0 0 -0.1", "0 0 0")))
xml.appendChild(createLink('right_leg_foot_link', createBlackMaterial(
), createBoxGeometry("0.05 0.05 0.05"), createOrigin("0 0 0", "0 0 0")))
xml.appendChild(createLink('right_leg_instep_link', createWhiteMaterial(
), createCylinderGeometry(0.015, 0.1), createOrigin("0.05 0 -0.02", "0 1.57 0")))


xml.appendChild(createFixedJoint('right_shoulder_joint', 'torso_link',
                'right_shoulder_link', createOrigin("0 -0.02 0.07", "0 0 0")))
xml.appendChild(createRevoluteJoint('right_upper_arm_joint', 'right_shoulder_up_link',
                'right_upper_arm_link', createOrigin("0 0 -0.05", "0 0 0"), "0 0 1"))
xml.appendChild(createRevoluteJoint('right_lower_arm_joint', 'right_elbow_link',
                'right_lower_arm_link', createOrigin("0 0 -0.05", "0 0 0"), "0 0 1"))
xml.appendChild(createRevoluteJoint('right_shoulder_forward_joint', 'right_shoulder_link',
                'right_shoulder_forward_link', createOrigin("0 -0.025 0", "0 0 0"), "1 0 0"))
xml.appendChild(createRevoluteJoint('right_shoulder_up_joint', 'right_shoulder_forward_link',
                'right_shoulder_up_link', createOrigin("0 -0.04 -0.01", "0 0 0"), "0 1 0"))
xml.appendChild(createRevoluteJoint('right_elbow_joint', 'right_upper_arm_link',
                'right_elbow_link', createOrigin("0 0 -0.05", "0 0 0"), "0 1 0"))
xml.appendChild(createRevoluteJoint('right_wrist_joint', 'right_lower_arm_link',
                'right_wrist_link', createOrigin("0 0 -0.05", "0 0 0"), "1 0 0"))

# 脚
xml.appendChild(createRevoluteJoint('right_leg_up_joint', 'base_rotation_link',
                'right_leg_up_link', createOrigin("0 -0.05 -0.05", "0 0 0"), "1 0 0"))
xml.appendChild(createRevoluteJoint('right_leg_lap_joint', 'right_leg_up_link',
                'right_leg_lap_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))
xml.appendChild(createFixedJoint('right_leg_knee_joint', 'right_leg_lap_link',
                'right_leg_knee_link', createOrigin("0 0 -0.2", "0 0 0")))
xml.appendChild(createRevoluteJoint('right_leg_shank_joint', 'right_leg_knee_link',
                'right_leg_shank_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))
xml.appendChild(createFixedJoint('right_leg_foot_joint', 'right_leg_shank_link',
                'right_leg_foot_link', createOrigin("0 0 -0.2", "0 0 0")))
xml.appendChild(createRevoluteJoint('right_leg_instep_joint', 'right_leg_foot_link',
                'right_leg_instep_link', createOrigin("0 0 0", "0 0 0"), "0 1 0"))


root.appendChild(xml)

xml_str = root.toprettyxml(indent="\t")


print(xml_str)

with open('Kibo-chan.urdf', mode='w', encoding='utf-8') as f:
    f.write(xml_str)
