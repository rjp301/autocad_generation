def space_points(points,spacing,iterations=5):
    """Function to intelligently space out a list of points 
    such that they are as close to their original positions 
    as possible while maintaining a certain buffer from one
    another
    
    These points are on a linear scale
    """

    def space(group,spacing):
        """Function to evenly space points around the
        centroid of the original group"""
        center = sum(group) / len(group) # determine center of group
        final_width = (len(group)-1) * spacing
        beg = center - final_width/2
        return [beg + i * spacing for i in range(len(group))]

    def clump(points,spacing):
        """Function to group points together based on 
        their proximity to one another"""
        points.sort()
        groups = [[pt] for pt in points]
        clumped_groups = []
        cand = groups.pop(0)
        while groups:
            spaced_cand = space(cand,spacing)
            if spaced_cand[-1] + spacing > groups[0][0]:
                cand += groups.pop(0)
            else:
                clumped_groups.append(cand)
                cand = groups.pop(0)
        clumped_groups.append(cand)
        return clumped_groups

    for _ in range(iterations):
        clumps = clump(points,spacing)
        result = []
        for item in clumps:
            result += space(item,spacing)
        points = result
    return result

def space_ranges(ranges,spacing,sort_by):
    """ sort_by = 0 for smallest
        sort_by = 1 for largest
        sort_by = 2 for center """ 
    ranges = [(min(i),max(i),sum(i)/len(i),max(i)-min(i)) for i in ranges]
    # (start,end,center,width)

    def space(group,spacing):
        """Function to evenly space points around the
        centroid of the original group"""
        center = sum([i[2] for i in group])/len(group)
        width = sum([i[3] for i in group]) + spacing * (len(group) - 1)
        group.sort(key=lambda i: i[sort_by])
        beg = center - width/2
        new_rngs = []
        for rng in group:
            new_rngs.append((beg,beg+rng[3],beg+rng[3]/2,rng[3]))
            beg += rng[3] + spacing
        return new_rngs

    def clump(ranges,spacing):
        """Function to group points together based on 
        their proximity to one another"""
        ranges.sort(key=lambda i: i[sort_by])
        groups = [[i] for i in ranges]
        clumped_groups = []
        cand = groups.pop(0)
        while groups:
            spaced_cand = space(cand,spacing)
            if spaced_cand[-1][1] + spacing > groups[0][0][0]:
                cand += groups.pop(0)
            else:
                clumped_groups.append(cand)
                cand = groups.pop(0)
        clumped_groups.append(cand)
        return clumped_groups

    for _ in range(50):
        clumps = clump(ranges,spacing)
        result = []
        for item in clumps:
            result += space(item,spacing)
        ranges = result

    return [(i[0],i[1]) for i in result]