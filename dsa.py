from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                  Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.colors import HexColor
import textwrap

# ── colour palette ──────────────────────────────────────────────────────────
C_DARK    = HexColor("#1a1a2e")   # deep navy
C_PRIMARY = HexColor("#16213e")   # section headers
C_ACCENT  = HexColor("#0f3460")   # subsection bars
C_TEAL    = HexColor("#00b4d8")   # accent / dividers
C_LIGHT   = HexColor("#e8f4f8")   # code background
C_ORANGE  = HexColor("#e94560")   # problem number tag
C_GREEN   = HexColor("#06d6a0")   # complexity badge
C_YELLOW  = HexColor("#ffd166")   # insight box
C_WHITE   = HexColor("#ffffff")
C_GRAY    = HexColor("#6c757d")
C_BG      = HexColor("#f0f4f8")   # page background band

WIDTH, HEIGHT = A4

# ── document setup ───────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Comprehensive_DSA_Practice_Guide.pdf",
    pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=2.2*cm,   bottomMargin=2*cm,
)

# ── styles ───────────────────────────────────────────────────────────────────
SS = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=SS[parent], **kw)
    return s

ST = {
    "title":     style("title",  "Title",
                       fontSize=32, textColor=C_WHITE, leading=38,
                       alignment=TA_CENTER, spaceAfter=6),
    "subtitle":  style("subtitle", "Normal",
                       fontSize=13, textColor=HexColor("#90e0ef"),
                       alignment=TA_CENTER, spaceAfter=4),
    "chapter":   style("chapter", "Heading1",
                       fontSize=20, textColor=C_WHITE, leading=26,
                       spaceBefore=6, spaceAfter=4, alignment=TA_CENTER),
    "section":   style("section", "Heading2",
                       fontSize=14, textColor=C_WHITE, leading=20,
                       spaceBefore=8, spaceAfter=4),
    "prob_title":style("prob_title","Heading3",
                       fontSize=12, textColor=C_DARK, leading=16,
                       spaceBefore=4, spaceAfter=3, fontName="Helvetica-Bold"),
    "label":     style("label", "Normal",
                       fontSize=9, textColor=C_TEAL, fontName="Helvetica-Bold",
                       spaceBefore=5, spaceAfter=2, leading=12),
    "body":      style("body", "Normal",
                       fontSize=9.5, textColor=C_DARK, leading=14,
                       spaceAfter=4, alignment=TA_JUSTIFY),
    "code":      style("code", "Normal",
                       fontSize=8, fontName="Courier", textColor=HexColor("#1d3557"),
                       leading=11, spaceAfter=3,
                       leftIndent=8, rightIndent=8),
    "insight":   style("insight","Normal",
                       fontSize=9, textColor=HexColor("#3d405b"),
                       leading=13, leftIndent=10, rightIndent=10, spaceAfter=3),
    "toc_ch":    style("toc_ch","Normal",
                       fontSize=11, textColor=C_PRIMARY, fontName="Helvetica-Bold",
                       spaceBefore=8, spaceAfter=2, leading=14),
    "toc_item":  style("toc_item","Normal",
                       fontSize=9, textColor=C_DARK, leading=13,
                       leftIndent=14, spaceAfter=1),
    "normal_c":  style("normal_c","Normal",
                       fontSize=9.5, textColor=C_DARK, leading=14, spaceAfter=3),
}

# ── helpers ──────────────────────────────────────────────────────────────────
def hline(color=C_TEAL, thickness=1.2):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def chapter_header(text):
    data = [[Paragraph(text, ST["chapter"])]]
    t = Table(data, colWidths=[WIDTH - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_PRIMARY),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[C_PRIMARY]),
        ("TOPPADDING",(0,0),(-1,-1),10),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(0,0),(-1,-1),14),
        ("ROUNDEDCORNERS",[6]),
    ]))
    return t

def section_header(text):
    data = [[Paragraph(text, ST["section"])]]
    t = Table(data, colWidths=[WIDTH - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), C_ACCENT),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),12),
    ]))
    return t

def prob_header(num, title, difficulty, category):
    diff_color = {"Easy": HexColor("#06d6a0"), "Medium": HexColor("#ffd166"), "Hard": HexColor("#e94560")}.get(difficulty, C_GRAY)
    left  = Paragraph(f'<font color="#e94560"><b>#{num}</b></font>  <b>{title}</b>', ST["prob_title"])
    right = Paragraph(f'<font color="{diff_color.hexval() if hasattr(diff_color,"hexval") else difficulty}"><b>{difficulty}</b></font><br/><font size="8" color="{C_GRAY.hexval()}">{category}</font>', ST["normal_c"])
    data = [[left, right]]
    t = Table(data, colWidths=[WIDTH*0.68 - 1.8*cm, WIDTH*0.32 - 0*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), C_BG),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LINEBELOW",(0,0),(-1,-1),2, C_TEAL),
    ]))
    return t

def code_block(code_str):
    lines = code_str.strip().split("\n")
    paras = [Paragraph(line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                       .replace(" ","&nbsp;"), ST["code"]) for line in lines]
    data = [[p] for p in paras]
    t = Table(data, colWidths=[WIDTH - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), C_LIGHT),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),1),
        ("BOTTOMPADDING",(0,0),(-1,-1),1),
        ("LINEAFTER", (0,0),(0,-1),3,C_TEAL),  # left accent bar
    ]))
    return t

def insight_box(text):
    data = [[Paragraph("💡  " + text, ST["insight"])]]
    t = Table(data, colWidths=[WIDTH - 3.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), HexColor("#fff8e7")),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("LINEAFTER",(0,0),(0,-1),4, C_YELLOW),
    ]))
    return t

def label(text): return Paragraph(text, ST["label"])
def body(text):  return Paragraph(text, ST["body"])
def sp(n=6):     return Spacer(1, n)

# ── problem builder ──────────────────────────────────────────────────────────
def problem(num, title, difficulty, category,
            statement, examples, approach, complexity,
            pseudocode, java_code, test_cases, insight_text):
    elems = []
    elems.append(sp(4))
    elems.append(prob_header(num, title, difficulty, category))
    elems.append(sp(4))

    elems.append(label("📋  PROBLEM STATEMENT"))
    elems.append(body(statement))

    elems.append(label("📌  EXAMPLES"))
    for ex in examples:
        elems.append(code_block(ex))

    elems.append(label("🧠  APPROACH"))
    elems.append(body(approach))
    elems.append(body(f"<b>Complexity:</b>  {complexity}"))

    elems.append(label("📝  PSEUDOCODE"))
    elems.append(code_block(pseudocode))

    elems.append(label("☕  JAVA IMPLEMENTATION"))
    elems.append(code_block(java_code))

    elems.append(label("✅  TEST CASES"))
    for tc in test_cases:
        elems.append(body(f"• {tc}"))

    elems.append(sp(3))
    elems.append(insight_box(insight_text))
    elems.append(hline())
    return elems

# ════════════════════════════════════════════════════════════════════════════
# PROBLEM DATA
# ════════════════════════════════════════════════════════════════════════════

problems = []

# ── SECTION 1: Arrays & Strings ──────────────────────────────────────────────
problems.append(("ARRAYS & STRINGS", None, None))

problems.append((1,"Two Sum","Easy","Arrays",
"Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume each input has exactly one solution.",
["Input: nums=[2,7,11,15], target=9\nOutput: [0,1]  (nums[0]+nums[1]=9)",
 "Input: nums=[3,2,4], target=6\nOutput: [1,2]"],
"Use a HashMap to store each element's value→index as we iterate. For each element, check if (target - current) exists in the map. This avoids a nested loop.",
"Time: O(n) | Space: O(n)",
"""function twoSum(nums, target):
    map = empty HashMap
    for i from 0 to len(nums)-1:
        complement = target - nums[i]
        if complement in map:
            return [map[complement], i]
        map[nums[i]] = i
    return []""",
"""import java.util.HashMap;
public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        HashMap<Integer,Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement))
                return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
["[2,7,11,15], target=9 → [0,1]","[3,2,4], target=6 → [1,2]","[3,3], target=6 → [0,1]","[] → [] (empty array)"],
"HashMap lookup is O(1) amortised. This classic problem illustrates the space-time tradeoff: one extra pass + O(n) space eliminates the O(n²) brute force."))

problems.append((2,"Best Time to Buy and Sell Stock","Easy","Arrays",
"Given an array prices where prices[i] is the price on day i, return the maximum profit from one buy-sell transaction. Return 0 if no profit possible.",
["Input: prices=[7,1,5,3,6,4]\nOutput: 5  (buy day2=1, sell day5=6)","Input: prices=[7,6,4,3,1]\nOutput: 0"],
"Track the minimum price seen so far and the maximum profit. One linear pass suffices — update minPrice and maxProfit at each step.",
"Time: O(n) | Space: O(1)",
"""function maxProfit(prices):
    minPrice = INF
    maxProfit = 0
    for price in prices:
        minPrice  = min(minPrice, price)
        maxProfit = max(maxProfit, price - minPrice)
    return maxProfit""",
"""public class BuyStock {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE, maxProfit = 0;
        for (int p : prices) {
            minPrice  = Math.min(minPrice, p);
            maxProfit = Math.max(maxProfit, p - minPrice);
        }
        return maxProfit;
    }
}""",
["[7,1,5,3,6,4] → 5","[7,6,4,3,1] → 0","[1] → 0","[2,4,1] → 2"],
"Greedy insight: the best sell day's profit equals (price - global minimum before that day). No need to track pairs explicitly."))

problems.append((3,"Contains Duplicate","Easy","Arrays",
"Given an integer array nums, return true if any value appears at least twice.",
["Input: [1,2,3,1] → true","Input: [1,2,3,4] → false"],
"Insert elements into a HashSet. If an element is already present, return true immediately.",
"Time: O(n) | Space: O(n)",
"""function containsDuplicate(nums):
    seen = empty Set
    for n in nums:
        if n in seen: return true
        seen.add(n)
    return false""",
"""import java.util.HashSet;
public class ContainsDuplicate {
    public boolean containsDuplicate(int[] nums) {
        HashSet<Integer> seen = new HashSet<>();
        for (int n : nums) {
            if (!seen.add(n)) return true;
        }
        return false;
    }
}""",
["[1,2,3,1] → true","[1,2,3,4] → false","[] → false","[1] → false","[1,1,1,3,3,4,3,2,4,2] → true"],
"HashSet.add() returns false if the element already exists — a neat one-liner check. Sorting the array then checking adjacent pairs also works in O(n log n) / O(1) space."))

problems.append((4,"Product of Array Except Self","Medium","Arrays",
"Given integer array nums, return array answer where answer[i] is the product of all elements except nums[i]. Must run in O(n) without division.",
["Input: [1,2,3,4]\nOutput: [24,12,8,6]","Input: [-1,1,0,-3,3]\nOutput: [0,0,9,0,0]"],
"Two-pass prefix/suffix product approach. First pass: build prefix products. Second pass: multiply with suffix products accumulated on the fly.",
"Time: O(n) | Space: O(1) extra (output array doesn't count)",
"""function productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
    // left pass
    prefix = 1
    for i in 0..n-1:
        result[i] = prefix
        prefix *= nums[i]
    // right pass
    suffix = 1
    for i in n-1..0:
        result[i] *= suffix
        suffix *= nums[i]
    return result""",
"""public class ProductExceptSelf {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        int prefix = 1;
        for (int i = 0; i < n; i++) { res[i] = prefix; prefix *= nums[i]; }
        int suffix = 1;
        for (int i = n-1; i >= 0; i--) { res[i] *= suffix; suffix *= nums[i]; }
        return res;
    }
}""",
["[1,2,3,4] → [24,12,8,6]","[-1,1,0,-3,3] → [0,0,9,0,0]","[0,0] → [0,0]","[1] → [1]"],
"Classic prefix-suffix trick. Think of each element's answer as (product of everything left) × (product of everything right). Combine the two in O(n) with O(1) extra space."))

problems.append((5,"Maximum Subarray","Medium","Arrays",
"Find the subarray with the largest sum and return its sum (Kadane's Algorithm).",
["Input: [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6  (subarray [4,-1,2,1])"],
"Kadane's: keep a running sum. If adding the current element improves it, extend; otherwise start fresh. Track global maximum.",
"Time: O(n) | Space: O(1)",
"""function maxSubArray(nums):
    curSum = maxSum = nums[0]
    for n in nums[1..]:
        curSum = max(n, curSum + n)
        maxSum = max(maxSum, curSum)
    return maxSum""",
"""public class MaxSubArray {
    public int maxSubArray(int[] nums) {
        int cur = nums[0], max = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            max = Math.max(max, cur);
        }
        return max;
    }
}""",
["[-2,1,-3,4,-1,2,1,-5,4] → 6","[1] → 1","[5,4,-1,7,8] → 23","[-1,-2,-3] → -1"],
"Kadane's algorithm is a DP where the state is 'best subarray ending here'. If the running sum becomes negative, it can never help future sums — reset to current element."))

problems.append((6,"Merge Intervals","Medium","Arrays",
"Given an array of intervals, merge all overlapping intervals and return the result.",
["Input: [[1,3],[2,6],[8,10],[15,18]]\nOutput: [[1,6],[8,10],[15,18]]"],
"Sort by start time. Then iterate: if current interval overlaps previous merged interval (curr.start <= prev.end), expand end. Otherwise push as new interval.",
"Time: O(n log n) | Space: O(n)",
"""function merge(intervals):
    sort intervals by start
    merged = [intervals[0]]
    for each interval in intervals[1..]:
        last = merged.last
        if interval.start <= last.end:
            last.end = max(last.end, interval.end)
        else:
            merged.append(interval)
    return merged""",
"""import java.util.Arrays;
import java.util.ArrayList;
public class MergeIntervals {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[0]-b[0]);
        ArrayList<int[]> res = new ArrayList<>();
        int[] cur = intervals[0];
        res.add(cur);
        for (int[] iv : intervals) {
            if (iv[0] <= cur[1]) cur[1] = Math.max(cur[1], iv[1]);
            else { cur = iv; res.add(cur); }
        }
        return res.toArray(new int[0][]);
    }
}""",
["[[1,3],[2,6]] → [[1,6]]","[[1,4],[4,5]] → [[1,5]]","[[1,4],[2,3]] → [[1,4]]","[[1,4],[5,6]] → [[1,4],[5,6]]"],
"Sorting turns an overlap problem into a simple linear scan. After sorting by start time, two intervals either overlap (merge) or are disjoint (append)."))

# ── SECTION 2: Two Pointers & Sliding Window ──────────────────────────────────
problems.append(("TWO POINTERS & SLIDING WINDOW", None, None))

problems.append((7,"Valid Palindrome","Easy","Two Pointers",
"A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward.",
["Input: 'A man, a plan, a canal: Panama' → true","Input: 'race a car' → false"],
"Two-pointer approach from both ends. Skip non-alphanumeric characters and compare lowercased characters.",
"Time: O(n) | Space: O(1)",
"""function isPalindrome(s):
    l, r = 0, len(s)-1
    while l < r:
        while l < r and not alnum(s[l]): l++
        while l < r and not alnum(s[r]): r--
        if lower(s[l]) != lower(s[r]): return false
        l++; r--
    return true""",
"""public class ValidPalindrome {
    public boolean isPalindrome(String s) {
        int l = 0, r = s.length()-1;
        while (l < r) {
            while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
            while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
            if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r)))
                return false;
            l++; r--;
        }
        return true;
    }
}""",
["'A man, a plan, a canal: Panama' → true","'race a car' → false","'' → true","'a' → true"],
"Two-pointer palindrome check is O(1) space. The key insight: move pointers inward, skipping irrelevant characters, comparing only alphanumerics."))

problems.append((8,"3Sum","Medium","Two Pointers",
"Given integer array nums, return all triplets [nums[i], nums[j], nums[k]] such that i≠j≠k and nums[i]+nums[j]+nums[k]==0.",
["Input: [-1,0,1,2,-1,-4]\nOutput: [[-1,-1,2],[-1,0,1]]"],
"Sort the array. Fix one element, then use two-pointer on the rest. Skip duplicates carefully to avoid repeats.",
"Time: O(n²) | Space: O(n) for output",
"""function threeSum(nums):
    sort(nums)
    result = []
    for i in 0..len(nums)-3:
        if i>0 and nums[i]==nums[i-1]: continue  // skip dup
        l, r = i+1, len(nums)-1
        while l < r:
            s = nums[i]+nums[l]+nums[r]
            if s == 0:
                result.add([nums[i],nums[l],nums[r]])
                while l<r and nums[l]==nums[l+1]: l++
                while l<r and nums[r]==nums[r-1]: r--
                l++; r--
            elif s < 0: l++
            else: r--
    return result""",
"""import java.util.*;
public class ThreeSum {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        for (int i = 0; i < nums.length-2; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;
            int l = i+1, r = nums.length-1;
            while (l < r) {
                int s = nums[i]+nums[l]+nums[r];
                if (s == 0) {
                    res.add(Arrays.asList(nums[i],nums[l],nums[r]));
                    while (l<r && nums[l]==nums[l+1]) l++;
                    while (l<r && nums[r]==nums[r-1]) r--;
                    l++; r--;
                } else if (s < 0) l++; else r--;
            }
        }
        return res;
    }
}""",
["[-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]","[0,0,0] → [[0,0,0]]","[0,1,1] → []","[] → []"],
"Sorting + two-pointer reduces 3Sum from O(n³) brute force to O(n²). Duplicate skipping is critical: check both the outer loop index and the inner pointers after recording a result."))

problems.append((9,"Longest Substring Without Repeating Characters","Medium","Sliding Window",
"Given a string s, find the length of the longest substring without repeating characters.",
["Input: 'abcabcbb' → 3 ('abc')","Input: 'bbbbb' → 1","Input: 'pwwkew' → 3 ('wke')"],
"Sliding window with a HashMap storing last seen index of each character. When a repeat is found, shrink window by moving left pointer past the duplicate.",
"Time: O(n) | Space: O(min(n,m)) where m is charset size",
"""function lengthOfLongestSubstring(s):
    map = {}  // char -> last index
    left = 0, maxLen = 0
    for right in 0..len(s)-1:
        if s[right] in map and map[s[right]] >= left:
            left = map[s[right]] + 1
        map[s[right]] = right
        maxLen = max(maxLen, right - left + 1)
    return maxLen""",
"""import java.util.HashMap;
public class LongestSubstring {
    public int lengthOfLongestSubstring(String s) {
        HashMap<Character,Integer> map = new HashMap<>();
        int left = 0, max = 0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            if (map.containsKey(c) && map.get(c) >= left)
                left = map.get(c) + 1;
            map.put(c, r);
            max = Math.max(max, r - left + 1);
        }
        return max;
    }
}""",
["'abcabcbb' → 3","'bbbbb' → 1","'pwwkew' → 3","'' → 0","'au' → 2"],
"The sliding window pattern: expand right freely, shrink left only when a constraint is violated. The HashMap lets us jump left pointer directly to the correct position — no slow incremental shrink needed."))

problems.append((10,"Minimum Window Substring","Hard","Sliding Window",
"Given strings s and t, return the minimum window substring of s that contains every character of t. Return empty string if no such window exists.",
["Input: s='ADOBECODEBANC', t='ABC'\nOutput: 'BANC'"],
"Use two pointers with frequency maps. Expand right until window is valid (contains all t chars). Then contract left to minimize. Track minimum window throughout.",
"Time: O(s+t) | Space: O(s+t)",
"""function minWindow(s, t):
    need = frequency map of t
    have, total = 0, len(unique chars in t)
    window = {}
    res, resLen = [-1,0], INF
    l = 0
    for r in 0..len(s)-1:
        c = s[r]; window[c]++
        if c in need and window[c] == need[c]: have++
        while have == total:
            if r-l+1 < resLen: res=[l,r]; resLen=r-l+1
            window[s[l]]--
            if s[l] in need and window[s[l]] < need[s[l]]: have--
            l++
    return s[res[0]:res[1]+1] if resLen != INF else ''""",
"""import java.util.HashMap;
public class MinWindowSubstring {
    public String minWindow(String s, String t) {
        if (s.isEmpty() || t.isEmpty()) return "";
        HashMap<Character,Integer> need = new HashMap<>(), win = new HashMap<>();
        for (char c : t.toCharArray()) need.merge(c,1,Integer::sum);
        int have=0, total=need.size(), l=0, minLen=Integer.MAX_VALUE, start=0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            win.merge(c,1,Integer::sum);
            if (need.containsKey(c) && win.get(c).equals(need.get(c))) have++;
            while (have == total) {
                if (r-l+1 < minLen) { minLen=r-l+1; start=l; }
                char lc = s.charAt(l++);
                win.merge(lc,-1,Integer::sum);
                if (need.containsKey(lc) && win.get(lc) < need.get(lc)) have--;
            }
        }
        return minLen==Integer.MAX_VALUE ? "" : s.substring(start, start+minLen);
    }
}""",
["s='ADOBECODEBANC',t='ABC' → 'BANC'","s='a',t='a' → 'a'","s='a',t='aa' → ''","s='aa',t='aa' → 'aa'"],
"The 'at least' constraint (need all chars of t) drives the shrink condition. Tracking 'have' vs 'total' avoids recomputing validity from scratch each iteration — key to the O(n) guarantee."))

# ── SECTION 3: Stack & Queue ──────────────────────────────────────────────────
problems.append(("STACKS & QUEUES", None, None))

problems.append((11,"Valid Parentheses","Easy","Stack",
"Given string s containing '(', ')', '{', '}', '[', ']', determine if the input string is valid. Open brackets must be closed in the correct order.",
["Input: '()[]{}' → true","Input: '(]' → false","Input: '([)]' → false"],
"Use a stack. Push open brackets. For each close bracket, check if stack top is the matching open bracket.",
"Time: O(n) | Space: O(n)",
"""function isValid(s):
    stack = []
    pairs = {')':'(', '}':'{', ']':'['}
    for c in s:
        if c in '({[': stack.push(c)
        else:
            if stack.empty or stack.top != pairs[c]: return false
            stack.pop()
    return stack.empty""",
"""import java.util.Stack;
public class ValidParentheses {
    public boolean isValid(String s) {
        Stack<Character> st = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c=='(' || c=='{' || c=='[') st.push(c);
            else {
                if (st.isEmpty()) return false;
                char t = st.pop();
                if ((c==')' && t!='(') || (c=='}' && t!='{') || (c==']' && t!='['))
                    return false;
            }
        }
        return st.isEmpty();
    }
}""",
["'()' → true","'()[]{}' → true","'(]' → false","'' → true","'[' → false"],
"Stack is the natural data structure for nested/matching problems. LIFO ensures that the most recently opened bracket is always checked first — exactly what valid nesting requires."))

problems.append((12,"Daily Temperatures","Medium","Stack (Monotonic)",
"Given array temperatures, return array answer where answer[i] is the number of days until a warmer temperature. If no future warmer day exists, answer[i]=0.",
["Input: [73,74,75,71,69,72,76,73]\nOutput: [1,1,4,2,1,1,0,0]"],
"Monotonic decreasing stack of indices. When a warmer temp is found, pop all cooler entries from the stack and record the difference.",
"Time: O(n) | Space: O(n)",
"""function dailyTemperatures(temps):
    stack = []  // indices
    result = [0] * len(temps)
    for i, t in enumerate(temps):
        while stack and temps[stack.top] < t:
            idx = stack.pop()
            result[idx] = i - idx
        stack.push(i)
    return result""",
"""import java.util.Stack;
public class DailyTemperatures {
    public int[] dailyTemperatures(int[] temps) {
        int[] res = new int[temps.length];
        Stack<Integer> st = new Stack<>();
        for (int i = 0; i < temps.length; i++) {
            while (!st.isEmpty() && temps[st.peek()] < temps[i]) {
                int idx = st.pop();
                res[idx] = i - idx;
            }
            st.push(i);
        }
        return res;
    }
}""",
["[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]","[30,40,50,60] → [1,1,1,0]","[30,60,90] → [1,1,0]"],
"Monotonic stacks excel at 'next greater element' problems. Maintain a stack that is always decreasing; any new element that breaks the order gives us the answer for all smaller stacked elements."))

problems.append((13,"Implement Queue using Stacks","Easy","Stack/Queue",
"Implement a first-in-first-out queue using only two stacks. Support push, pop, peek, and empty operations.",
["MyQueue q = new MyQueue(); q.push(1); q.push(2); q.peek()→1; q.pop()→1; q.empty()→false"],
"Use two stacks: inbox (push) and outbox (pop). Transfer from inbox to outbox lazily only when outbox is empty.",
"Amortised O(1) per operation | Space: O(n)",
"""class MyQueue:
    inbox, outbox = [], []
    push(x): inbox.push(x)
    pop():
        if outbox.empty: transfer()
        return outbox.pop()
    peek():
        if outbox.empty: transfer()
        return outbox.top
    transfer(): while inbox: outbox.push(inbox.pop())""",
"""import java.util.Stack;
public class MyQueue {
    Stack<Integer> in = new Stack<>(), out = new Stack<>();
    public void push(int x) { in.push(x); }
    public int pop()  { move(); return out.pop(); }
    public int peek() { move(); return out.peek(); }
    public boolean empty() { return in.isEmpty() && out.isEmpty(); }
    private void move() { if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop()); }
}""",
["push(1),push(2),pop()→1","push(1),peek()→1,pop()→1,empty()→true"],
"Two-stack queue achieves amortised O(1) because each element is moved at most once from inbox to outbox. Classic interview pattern demonstrating that amortised analysis can rescue seemingly expensive lazy operations."))

# ── SECTION 4: Linked List ───────────────────────────────────────────────────
problems.append(("LINKED LISTS", None, None))

problems.append((14,"Reverse Linked List","Easy","Linked List",
"Given the head of a singly linked list, reverse the list and return the reversed list.",
["Input: 1→2→3→4→5 → Output: 5→4→3→2→1"],
"Iterative: maintain prev pointer. Walk list, at each node flip the next pointer, then advance.",
"Time: O(n) | Space: O(1) iterative, O(n) recursive",
"""function reverseList(head):
    prev = null
    curr = head
    while curr != null:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev""",
"""public class ReverseLinkedList {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }
}""",
["1→2→3→4→5 → 5→4→3→2→1","1→2 → 2→1","null → null","1 → 1"],
"Pointer manipulation: think of 'prev' as the growing reversed list. At each step, detach current node, point it backward, advance. The three-pointer dance (prev/curr/next) is fundamental to linked list manipulation."))

problems.append((15,"Merge Two Sorted Lists","Easy","Linked List",
"Merge two sorted linked lists and return the merged list (sorted).",
["Input: 1→2→4,  1→3→4 → Output: 1→1→2→3→4→4"],
"Use a dummy head node and a pointer. Compare heads of both lists, attach smaller, advance that list's pointer.",
"Time: O(n+m) | Space: O(1)",
"""function mergeTwoLists(l1, l2):
    dummy = new Node(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val: curr.next=l1; l1=l1.next
        else:                curr.next=l2; l2=l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next""",
"""public class MergeTwoLists {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
            else                  { cur.next = l2; l2 = l2.next; }
            cur = cur.next;
        }
        cur.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }
}""",
["1→2→4, 1→3→4 → 1→1→2→3→4→4","[], 0 → 0","[], [] → []"],
"The dummy head trick avoids special-casing the first node. Appending the remaining list at the end is an O(1) operation since list nodes are already in order — no additional iteration needed."))

problems.append((16,"Detect Cycle in Linked List","Easy","Linked List / Two Pointers",
"Given the head of a linked list, determine if the linked list has a cycle.",
["Input: 3→2→0→-4→(back to 2) → true","Input: 1→2→null → false"],
"Floyd's cycle detection (tortoise and hare). Slow pointer moves 1 step, fast pointer moves 2 steps. They meet if and only if there's a cycle.",
"Time: O(n) | Space: O(1)",
"""function hasCycle(head):
    slow = fast = head
    while fast != null and fast.next != null:
        slow = slow.next
        fast = fast.next.next
        if slow == fast: return true
    return false""",
"""public class DetectCycle {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}""",
["Cycle present → true","No cycle → false","Single node, no cycle → false","Single node, self-loop → true"],
"Floyd's algorithm: if a cycle exists, fast pointer will 'lap' the slow one. Proof: distance between them decreases by 1 each step once both are in the cycle. Guaranteed meet in O(n) steps."))

problems.append((17,"LRU Cache","Medium","Linked List + HashMap",
"Design a data structure that follows the LRU (Least Recently Used) cache eviction policy with O(1) get and put operations.",
["LRUCache(2); put(1,1); put(2,2); get(1)→1; put(3,3); get(2)→-1"],
"Combine a doubly linked list (order by recency) and a HashMap (O(1) access by key). On access/insert, move node to front; evict from tail when capacity exceeded.",
"Time: O(1) per operation | Space: O(capacity)",
"""class LRUCache(capacity):
    map = HashMap<key, Node>
    DLL: dummy_head <-> ... <-> dummy_tail
    get(key):
        if key not in map: return -1
        moveToFront(map[key])
        return map[key].val
    put(key,val):
        if key in map: moveToFront; update val
        else:
            if size==capacity: evict tail; remove from map
            create new node; insertAtFront; map[key]=node""",
"""import java.util.HashMap;
public class LRUCache {
    class Node { int key,val; Node prev,next; Node(int k,int v){key=k;val=v;} }
    int cap; HashMap<Integer,Node> map = new HashMap<>();
    Node head = new Node(0,0), tail = new Node(0,0);
    public LRUCache(int c) { cap=c; head.next=tail; tail.prev=head; }
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node n = map.get(key); remove(n); insert(n); return n.val;
    }
    public void put(int k, int v) {
        if (map.containsKey(k)) remove(map.get(k));
        Node n = new Node(k,v); insert(n); map.put(k,n);
        if (map.size() > cap) { Node del=tail.prev; remove(del); map.remove(del.key); }
    }
    void remove(Node n){ n.prev.next=n.next; n.next.prev=n.prev; }
    void insert(Node n){ n.next=head.next; n.prev=head; head.next.prev=n; head.next=n; }
}""",
["capacity=2; put(1,1),put(2,2),get(1)=1,put(3,3),get(2)=-1,get(3)=3","Evict least recently used when full"],
"LRU Cache is a classic design problem. The DLL gives O(1) insertion/deletion from any position; the HashMap gives O(1) lookup. The two structures work together — the map holds node pointers, the list maintains order."))

# ── SECTION 5: Binary Search ──────────────────────────────────────────────────
problems.append(("BINARY SEARCH", None, None))

problems.append((18,"Binary Search","Easy","Binary Search",
"Given a sorted array of integers and a target, return the index of target or -1 if not found.",
["Input: nums=[-1,0,3,5,9,12], target=9 → 4","Input: nums=[-1,0,3,5,9,12], target=2 → -1"],
"Classic binary search: maintain lo and hi pointers, compute mid, compare with target, and halve the search space.",
"Time: O(log n) | Space: O(1)",
"""function binarySearch(nums, target):
    lo, hi = 0, len(nums)-1
    while lo <= hi:
        mid = lo + (hi-lo)//2
        if nums[mid] == target: return mid
        elif nums[mid] < target: lo = mid+1
        else: hi = mid-1
    return -1""",
"""public class BinarySearch {
    public int search(int[] nums, int target) {
        int lo = 0, hi = nums.length-1;
        while (lo <= hi) {
            int mid = lo + (hi-lo)/2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) lo = mid+1;
            else hi = mid-1;
        }
        return -1;
    }
}""",
["[-1,0,3,5,9,12], 9 → 4","[-1,0,3,5,9,12], 2 → -1","[5], 5 → 0","[5], 3 → -1"],
"Use mid = lo + (hi-lo)/2 instead of (lo+hi)/2 to avoid integer overflow. Binary search halves the search space each iteration: log₂(10⁹) ≈ 30 iterations to search a billion elements."))

problems.append((19,"Find Minimum in Rotated Sorted Array","Medium","Binary Search",
"Suppose an array of distinct integers is sorted and then rotated. Find the minimum element.",
["Input: [3,4,5,1,2] → 1","Input: [4,5,6,7,0,1,2] → 0"],
"Binary search: if mid > right, minimum is in right half. Otherwise it's in left half (including mid).",
"Time: O(log n) | Space: O(1)",
"""function findMin(nums):
    lo, hi = 0, len(nums)-1
    while lo < hi:
        mid = lo + (hi-lo)//2
        if nums[mid] > nums[hi]: lo = mid+1
        else: hi = mid
    return nums[lo]""",
"""public class FindMinRotated {
    public int findMin(int[] nums) {
        int lo = 0, hi = nums.length-1;
        while (lo < hi) {
            int mid = lo + (hi-lo)/2;
            if (nums[mid] > nums[hi]) lo = mid+1;
            else hi = mid;
        }
        return nums[lo];
    }
}""",
["[3,4,5,1,2] → 1","[4,5,6,7,0,1,2] → 0","[11,13,15,17] → 11","[1] → 1"],
"In a rotated sorted array, exactly one 'break point' exists. Comparing mid to hi tells us which half the minimum is in — the unsorted half always contains the minimum."))

problems.append((20,"Search in Rotated Sorted Array","Medium","Binary Search",
"Search for a target in a rotated sorted array. Return index or -1.",
["Input: nums=[4,5,6,7,0,1,2], target=0 → 4"],
"Determine which half is sorted, then check if target lies in that half. Binary search with two cases.",
"Time: O(log n) | Space: O(1)",
"""function search(nums, target):
    lo, hi = 0, len(nums)-1
    while lo <= hi:
        mid = lo + (hi-lo)//2
        if nums[mid] == target: return mid
        if nums[lo] <= nums[mid]:  // left half sorted
            if nums[lo] <= target < nums[mid]: hi = mid-1
            else: lo = mid+1
        else:  // right half sorted
            if nums[mid] < target <= nums[hi]: lo = mid+1
            else: hi = mid-1
    return -1""",
"""public class SearchRotated {
    public int search(int[] nums, int target) {
        int lo = 0, hi = nums.length-1;
        while (lo <= hi) {
            int mid = lo+(hi-lo)/2;
            if (nums[mid]==target) return mid;
            if (nums[lo]<=nums[mid]) {
                if (nums[lo]<=target && target<nums[mid]) hi=mid-1; else lo=mid+1;
            } else {
                if (nums[mid]<target && target<=nums[hi]) lo=mid+1; else hi=mid-1;
            }
        }
        return -1;
    }
}""",
["[4,5,6,7,0,1,2], 0 → 4","[4,5,6,7,0,1,2], 3 → -1","[1], 0 → -1","[1,3], 3 → 1"],
"The key invariant: at least one half of the array is always sorted. Use that sorted half to determine if the target could be there; otherwise search the other half."))

# ── SECTION 6: Trees ─────────────────────────────────────────────────────────
problems.append(("TREES & BST", None, None))

problems.append((21,"Maximum Depth of Binary Tree","Easy","Trees",
"Given the root of a binary tree, return its maximum depth.",
["Input: [3,9,20,null,null,15,7] → 3"],
"Recursive DFS: depth = 1 + max(depth(left), depth(right)). Base case: null node returns 0.",
"Time: O(n) | Space: O(h) where h is height",
"""function maxDepth(root):
    if root == null: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))""",
"""public class MaxDepth {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}""",
["[3,9,20,null,null,15,7] → 3","[] → 0","[1,null,2] → 2","[1] → 1"],
"Tree recursion naturally mirrors the tree structure. Every tree problem has a recursive substructure: solve for left subtree, solve for right subtree, combine. This is divide-and-conquer at its purest."))

problems.append((22,"Validate Binary Search Tree","Medium","BST",
"Given the root of a binary tree, determine if it is a valid BST.",
["Input: [2,1,3] → true","Input: [5,1,4,null,null,3,6] → false"],
"Pass min/max bounds down the recursion. Each node must be strictly within its allowed range.",
"Time: O(n) | Space: O(h)",
"""function isValidBST(root, min=-INF, max=INF):
    if root == null: return true
    if root.val <= min or root.val >= max: return false
    return isValidBST(root.left, min, root.val) and
           isValidBST(root.right, root.val, max)""",
"""public class ValidateBST {
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    private boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        if (node.val <= min || node.val >= max) return false;
        return validate(node.left, min, node.val) &&
               validate(node.right, node.val, max);
    }
}""",
["[2,1,3] → true","[5,1,4,null,null,3,6] → false","[1,1] → false (equal not allowed)"],
"Common mistake: only checking parent-child relationship isn't enough. [5,4,6,null,null,3,7] fails because node 3 violates the root constraint. The min/max bound propagation captures the full BST property."))

problems.append((23,"Level Order Traversal","Medium","Trees / BFS",
"Given a binary tree, return level-order traversal of its nodes' values as a list of lists.",
["Input: [3,9,20,null,null,15,7]\nOutput: [[3],[9,20],[15,7]]"],
"BFS with a queue. Process level by level: record queue size at start of each level, then process exactly that many nodes.",
"Time: O(n) | Space: O(n)",
"""function levelOrder(root):
    if not root: return []
    q = Queue([root])
    result = []
    while q not empty:
        level = []
        for _ in range(len(q)):  // process one level
            node = q.dequeue()
            level.append(node.val)
            if node.left:  q.enqueue(node.left)
            if node.right: q.enqueue(node.right)
        result.append(level)
    return result""",
"""import java.util.*;
public class LevelOrder {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            int size = q.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode n = q.poll();
                level.add(n.val);
                if (n.left  != null) q.offer(n.left);
                if (n.right != null) q.offer(n.right);
            }
            res.add(level);
        }
        return res;
    }
}""",
["[3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]","[] → []","[1] → [[1]]"],
"The 'snapshot the queue size' trick is key: by recording the queue length before processing a level, we avoid mixing nodes from different levels. This BFS pattern extends to zigzag traversal, right-side view, etc."))

problems.append((24,"Binary Tree Maximum Path Sum","Hard","Trees / DFS",
"A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. Return the maximum path sum (path can start and end at any node).",
["Input: [-10,9,20,null,null,15,7] → 42  (path: 15→20→7)","Input: [-3] → -3"],
"DFS returning the max gain through each node (single path going up). Internally track the max path that could use the node as the 'peak' (left + node + right).",
"Time: O(n) | Space: O(h)",
"""maxSum = -INF
function maxPathSum(root):
    dfs(root)
    return maxSum

function dfs(node):
    if node == null: return 0
    leftGain  = max(0, dfs(node.left))   // ignore negative paths
    rightGain = max(0, dfs(node.right))
    maxSum = max(maxSum, node.val + leftGain + rightGain)  // update global
    return node.val + max(leftGain, rightGain)  // return single path to parent""",
"""public class MaxPathSum {
    int max = Integer.MIN_VALUE;
    public int maxPathSum(TreeNode root) { dfs(root); return max; }
    int dfs(TreeNode n) {
        if (n == null) return 0;
        int l = Math.max(0, dfs(n.left));
        int r = Math.max(0, dfs(n.right));
        max = Math.max(max, n.val + l + r);
        return n.val + Math.max(l, r);
    }
}""",
["[-10,9,20,null,null,15,7] → 42","[-3] → -3","[1,-2,-3,1,3,-2,null,-1] → 3"],
"The return value vs global update split is classic tree DP: the recursive function returns the best single-branch path (to be used by the parent), while the global max considers the full 'arch' through the current node."))

# ── SECTION 7: Graphs ─────────────────────────────────────────────────────────
problems.append(("GRAPH ALGORITHMS", None, None))

problems.append((25,"Number of Islands","Medium","Graph / DFS",
"Given a 2D binary grid of '1's (land) and '0's (water), count the number of islands.",
["Input:\n['1','1','0'],\n['1','1','0'],\n['0','0','1']\nOutput: 2"],
"DFS from each unvisited land cell, marking visited cells. Each DFS call represents one island.",
"Time: O(m×n) | Space: O(m×n)",
"""function numIslands(grid):
    count = 0
    for i in rows:
        for j in cols:
            if grid[i][j]=='1':
                dfs(grid, i, j)
                count++
    return count

function dfs(grid, i, j):
    if out-of-bounds or grid[i][j]!='1': return
    grid[i][j] = '0'  // mark visited
    dfs(grid,i+1,j); dfs(grid,i-1,j)
    dfs(grid,i,j+1); dfs(grid,i,j-1)""",
"""public class NumIslands {
    public int numIslands(char[][] grid) {
        int count = 0;
        for (int i = 0; i < grid.length; i++)
            for (int j = 0; j < grid[0].length; j++)
                if (grid[i][j]=='1') { dfs(grid,i,j); count++; }
        return count;
    }
    void dfs(char[][] g, int i, int j) {
        if (i<0||j<0||i>=g.length||j>=g[0].length||g[i][j]!='1') return;
        g[i][j]='0';
        dfs(g,i+1,j); dfs(g,i-1,j); dfs(g,i,j+1); dfs(g,i,j-1);
    }
}""",
["All 1s → 1 island","All 0s → 0","Checkerboard → many","Single cell '1' → 1"],
"Flood fill / connected components in a grid. Modifying the grid in-place (marking visited) avoids a separate visited array. This DFS pattern generalises to any 2D connectivity problem."))

problems.append((26,"Clone Graph","Medium","Graph / DFS",
"Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.",
["Input: adjList=[[2,4],[1,3],[2,4],[1,3]] → deep copy of same structure"],
"DFS with a HashMap mapping original node → cloned node. Before recursing neighbours, create the clone and store in map to handle cycles.",
"Time: O(n+e) | Space: O(n)",
"""function cloneGraph(node, visited={}):
    if node == null: return null
    if node in visited: return visited[node]
    clone = new Node(node.val)
    visited[node] = clone
    for neighbor in node.neighbors:
        clone.neighbors.add(cloneGraph(neighbor, visited))
    return clone""",
"""import java.util.HashMap;
import java.util.ArrayList;
public class CloneGraph {
    HashMap<Node,Node> map = new HashMap<>();
    public Node cloneGraph(Node node) {
        if (node==null) return null;
        if (map.containsKey(node)) return map.get(node);
        Node clone = new Node(node.val, new ArrayList<>());
        map.put(node, clone);
        for (Node n : node.neighbors) clone.neighbors.add(cloneGraph(n));
        return clone;
    }
}""",
["Single node, no neighbours → single clone","Cycle of 2 nodes → two clones with edges","null → null"],
"The visited map serves dual purpose: memoization (avoid reprocessing) and cycle detection (return existing clone for already-seen nodes). Without it, cycles would cause infinite recursion."))

problems.append((27,"Course Schedule","Medium","Graph / Topological Sort",
"There are numCourses courses (0 to n-1). Given prerequisites pairs [a,b] meaning 'must take b before a', determine if it's possible to finish all courses.",
["Input: numCourses=2, prerequisites=[[1,0]] → true","Input: numCourses=2, prerequisites=[[1,0],[0,1]] → false"],
"Detect cycle in directed graph using DFS with 3 states: unvisited(0), visiting(1), visited(2). A back edge (visiting→visiting) indicates a cycle.",
"Time: O(V+E) | Space: O(V+E)",
"""function canFinish(n, prereqs):
    graph = build adjacency list
    state = [0] * n  // 0=unvisited, 1=visiting, 2=visited
    function dfs(node):
        if state[node]==1: return false  // cycle
        if state[node]==2: return true   // already processed
        state[node] = 1
        for neighbor in graph[node]:
            if not dfs(neighbor): return false
        state[node] = 2
        return true
    for i in 0..n-1:
        if not dfs(i): return false
    return true""",
"""import java.util.*;
public class CourseSchedule {
    public boolean canFinish(int n, int[][] prereqs) {
        List<List<Integer>> g = new ArrayList<>();
        for (int i=0;i<n;i++) g.add(new ArrayList<>());
        for (int[] p: prereqs) g.get(p[1]).add(p[0]);
        int[] state = new int[n];
        for (int i=0;i<n;i++) if (!dfs(g,state,i)) return false;
        return true;
    }
    boolean dfs(List<List<Integer>> g, int[] st, int node) {
        if (st[node]==1) return false;
        if (st[node]==2) return true;
        st[node]=1;
        for (int nb : g.get(node)) if (!dfs(g,st,nb)) return false;
        st[node]=2; return true;
    }
}""",
["No prereqs → true","Simple chain → true","Cycle → false","Disconnected components → each checked independently"],
"Course Schedule is cycle detection in a DAG. The 3-state coloring (white/gray/black) is the standard DFS cycle detection approach. Alternatively, use Kahn's BFS algorithm (in-degree based topological sort)."))

problems.append((28,"Word Ladder","Hard","Graph / BFS",
"Given beginWord, endWord, and a wordList, return the number of words in the shortest transformation sequence from beginWord to endWord (each step differs by one letter).",
["Input: beginWord='hit', endWord='cog', wordList=['hot','dot','dog','lot','log','cog']\nOutput: 5  (hit→hot→dot→dog→cog)"],
"BFS on implicit graph. Level = transformation step count. From each word, generate all possible one-letter variants and check if they're in the dictionary.",
"Time: O(n×L²) | Space: O(n×L) where n=words, L=word length",
"""function ladderLength(begin, end, wordList):
    wordSet = set(wordList)
    if end not in wordSet: return 0
    q = Queue([(begin, 1)])
    visited = {begin}
    while q not empty:
        word, steps = q.dequeue()
        for i in range(len(word)):
            for c in 'a'..'z':
                next = word[:i] + c + word[i+1:]
                if next == end: return steps+1
                if next in wordSet and next not in visited:
                    visited.add(next); q.enqueue((next, steps+1))
    return 0""",
"""import java.util.*;
public class WordLadder {
    public int ladderLength(String begin, String end, List<String> wordList) {
        Set<String> ws = new HashSet<>(wordList);
        if (!ws.contains(end)) return 0;
        Queue<String> q = new LinkedList<>(); q.offer(begin);
        Set<String> vis = new HashSet<>(); vis.add(begin);
        int steps = 1;
        while (!q.isEmpty()) {
            for (int sz = q.size(); sz > 0; sz--) {
                char[] w = q.poll().toCharArray();
                for (int i=0;i<w.length;i++) {
                    char orig = w[i];
                    for (char c='a';c<='z';c++) {
                        w[i]=c; String nw = new String(w);
                        if (nw.equals(end)) return steps+1;
                        if (ws.contains(nw)&&!vis.contains(nw)){vis.add(nw);q.offer(nw);}
                    }
                    w[i]=orig;
                }
            }
            steps++;
        }
        return 0;
    }
}""",
["hit→cog (wordList given) → 5","No path → 0","begin==end → 1"],
"Word Ladder models an unweighted shortest path problem on an implicit graph. BFS guarantees the shortest path. Generating neighbours by substituting each character position is the key graph-edge definition."))

# ── SECTION 8: Dynamic Programming ───────────────────────────────────────────
problems.append(("DYNAMIC PROGRAMMING", None, None))

problems.append((29,"Climbing Stairs","Easy","DP",
"You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?",
["n=2 → 2 (1+1 or 2)","n=3 → 3 (1+1+1, 1+2, 2+1)"],
"This is the Fibonacci sequence: ways(n) = ways(n-1) + ways(n-2). Use bottom-up DP with O(1) space.",
"Time: O(n) | Space: O(1)",
"""function climbStairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for i in 3..n:
        a, b = b, a+b
    return b""",
"""public class ClimbingStairs {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) { int c = a+b; a=b; b=c; }
        return b;
    }
}""",
["n=1 → 1","n=2 → 2","n=3 → 3","n=10 → 89","n=45 → 1134903170"],
"Climbing stairs is the 'hello world' of DP. The recurrence ways(n)=ways(n-1)+ways(n-2) comes from the last step being either 1 or 2. Recognize this as Fibonacci and optimise from O(n) space to O(1)."))

problems.append((30,"Coin Change","Medium","DP",
"Given coins of different denominations and a total amount, find the minimum number of coins needed to make up the amount. Return -1 if impossible.",
["coins=[1,5,11], amount=15 → 3 (5+5+5 or 11+1+1+1 is 4, best is 5+5+5)","coins=[2], amount=3 → -1"],
"Bottom-up DP: dp[i] = minimum coins to make amount i. For each amount, try all coins.",
"Time: O(n×amount) | Space: O(amount)",
"""function coinChange(coins, amount):
    dp = [INF] * (amount+1)
    dp[0] = 0
    for i in 1..amount:
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i-coin]+1)
    return dp[amount] if dp[amount] != INF else -1""",
"""import java.util.Arrays;
public class CoinChange {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount+1];
        Arrays.fill(dp, amount+1);
        dp[0] = 0;
        for (int i=1;i<=amount;i++)
            for (int c : coins)
                if (c<=i) dp[i]=Math.min(dp[i], dp[i-c]+1);
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
["[1,5,11],15 → 3","[2],3 → -1","[1],0 → 0","[1,2,5],11 → 3"],
"Unbounded knapsack variant. dp[i] = 'fewest coins for amount i'. The inner loop over coins asks: if I last used coin c, what was the cost to reach i-c? Build up from smaller amounts."))

problems.append((31,"Longest Common Subsequence","Medium","DP",
"Given two strings text1 and text2, return the length of their longest common subsequence.",
["text1='abcde', text2='ace' → 3 ('ace')","text1='abc', text2='abc' → 3","text1='abc', text2='def' → 0"],
"2D DP: dp[i][j] = LCS of text1[0..i-1] and text2[0..j-1]. If chars match, extend; otherwise take max of excluding either char.",
"Time: O(m×n) | Space: O(m×n)",
"""function LCS(text1, text2):
    m, n = len(text1), len(text2)
    dp = 2D array [m+1][n+1] filled with 0
    for i in 1..m:
        for j in 1..n:
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]""",
"""public class LCS {
    public int longestCommonSubsequence(String s1, String s2) {
        int m=s1.length(), n=s2.length();
        int[][] dp = new int[m+1][n+1];
        for (int i=1;i<=m;i++)
            for (int j=1;j<=n;j++)
                dp[i][j] = s1.charAt(i-1)==s2.charAt(j-1)
                           ? dp[i-1][j-1]+1
                           : Math.max(dp[i-1][j], dp[i][j-1]);
        return dp[m][n];
    }
}""",
["'abcde','ace' → 3","'abc','abc' → 3","'abc','def' → 0","'','abc' → 0"],
"LCS is fundamental to diff tools, bioinformatics, and version control. The recurrence elegantly handles both cases: characters match (extend) or don't (take best by dropping one char from either string)."))

problems.append((32,"0/1 Knapsack","Medium","DP",
"Given n items each with weight and value, and a knapsack of capacity W, find maximum value achievable without exceeding weight capacity. Each item can be used at most once.",
["items=[(2,3),(3,4),(4,5),(5,6)], W=5 → 7 (items 0+1)"],
"2D DP: dp[i][w] = max value using first i items with weight capacity w. For each item, choose to include or exclude.",
"Time: O(n×W) | Space: O(n×W), optimisable to O(W)",
"""function knapsack(weights, values, W):
    n = len(weights)
    dp = 2D [n+1][W+1] filled with 0
    for i in 1..n:
        for w in 0..W:
            dp[i][w] = dp[i-1][w]  // exclude
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])
    return dp[n][W]""",
"""public class Knapsack {
    public int knapsack(int[] weights, int[] values, int W) {
        int n = weights.length;
        int[][] dp = new int[n+1][W+1];
        for (int i=1;i<=n;i++)
            for (int w=0;w<=W;w++) {
                dp[i][w] = dp[i-1][w];
                if (weights[i-1]<=w)
                    dp[i][w] = Math.max(dp[i][w], dp[i-1][w-weights[i-1]]+values[i-1]);
            }
        return dp[n][W];
    }
}""",
["W=5, wt=[2,3,4,5], val=[3,4,5,6] → 7","W=0 → 0","Single item fits → item value","Single item too heavy → 0"],
"0/1 Knapsack is the archetype of include/exclude DP. Space can be optimised to O(W) by iterating w in reverse (to avoid using the same item twice). This is the parent problem for subset sum, partition equal subset, etc."))

problems.append((33,"Word Break","Medium","DP",
"Given string s and dictionary wordDict, return true if s can be segmented into space-separated dictionary words.",
["s='leetcode', wordDict=['leet','code'] → true","s='applepenapple', wordDict=['apple','pen'] → true","s='catsandog', wordDict=['cats','dog','sand','and','cat'] → false"],
"DP: dp[i]=true if s[0..i-1] can be segmented. For each position, check all words that end at i.",
"Time: O(n²×m) | Space: O(n)",
"""function wordBreak(s, wordDict):
    n = len(s)
    ws = set(wordDict)
    dp = [false] * (n+1)
    dp[0] = true
    for i in 1..n:
        for j in 0..i-1:
            if dp[j] and s[j:i] in ws:
                dp[i] = true; break
    return dp[n]""",
"""import java.util.*;
public class WordBreak {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> ws = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length()+1];
        dp[0] = true;
        for (int i=1;i<=s.length();i++)
            for (int j=0;j<i;j++)
                if (dp[j] && ws.contains(s.substring(j,i))) { dp[i]=true; break; }
        return dp[s.length()];
    }
}""",
["'leetcode',['leet','code'] → true","'applepenapple',['apple','pen'] → true","'catsandog',['cats','dog'] → false"],
"dp[i] represents 'can we reach position i via valid words'. The inner loop checks all possible last words ending at i. Trie can speed up word lookup for long dictionaries."))

problems.append((34,"Edit Distance","Hard","DP",
"Given two strings word1 and word2, return the minimum number of operations (insert, delete, replace) to convert word1 to word2.",
["word1='horse', word2='ros' → 3","word1='intention', word2='execution' → 5"],
"Classic 2D DP (Levenshtein). dp[i][j] = min operations to convert word1[0..i-1] to word2[0..j-1].",
"Time: O(m×n) | Space: O(m×n)",
"""function editDistance(w1, w2):
    m, n = len(w1), len(w2)
    dp = 2D [m+1][n+1]
    for i: dp[i][0] = i  // delete all of w1
    for j: dp[0][j] = j  // insert all of w2
    for i in 1..m:
        for j in 1..n:
            if w1[i-1] == w2[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j],   // delete
                                     dp[i][j-1],   // insert
                                     dp[i-1][j-1]) // replace""",
"""public class EditDistance {
    public int minDistance(String w1, String w2) {
        int m=w1.length(), n=w2.length();
        int[][] dp = new int[m+1][n+1];
        for (int i=0;i<=m;i++) dp[i][0]=i;
        for (int j=0;j<=n;j++) dp[0][j]=j;
        for (int i=1;i<=m;i++)
            for (int j=1;j<=n;j++)
                dp[i][j] = w1.charAt(i-1)==w2.charAt(j-1) ? dp[i-1][j-1]
                           : 1+Math.min(dp[i-1][j], Math.min(dp[i][j-1], dp[i-1][j-1]));
        return dp[m][n];
    }
}""",
["'horse','ros' → 3","'intention','execution' → 5","'','abc' → 3","'abc','abc' → 0"],
"Levenshtein distance powers spell checkers, DNA sequence alignment, and fuzzy matching. Three edit operations map to three DP transitions: delete (come from left), insert (come from above), replace (come from diagonal)."))

# ── SECTION 9: Backtracking ───────────────────────────────────────────────────
problems.append(("BACKTRACKING", None, None))

problems.append((35,"Subsets","Medium","Backtracking",
"Given an integer array nums of unique elements, return all possible subsets (the power set).",
["Input: [1,2,3]\nOutput: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"],
"Backtracking: at each element, choose to include or not. Alternatively, iterative bit-mask or cascade approach.",
"Time: O(n × 2^n) | Space: O(n × 2^n)",
"""function subsets(nums):
    result = []
    function backtrack(start, current):
        result.append(copy of current)
        for i in start..len(nums)-1:
            current.append(nums[i])
            backtrack(i+1, current)
            current.removeLast()
    backtrack(0, [])
    return result""",
"""import java.util.*;
public class Subsets {
    List<List<Integer>> res = new ArrayList<>();
    public List<List<Integer>> subsets(int[] nums) {
        backtrack(nums, 0, new ArrayList<>());
        return res;
    }
    void backtrack(int[] nums, int start, List<Integer> cur) {
        res.add(new ArrayList<>(cur));
        for (int i=start;i<nums.length;i++) {
            cur.add(nums[i]);
            backtrack(nums, i+1, cur);
            cur.remove(cur.size()-1);
        }
    }
}""",
["[1,2,3] → 8 subsets","[] → [[]]","[1] → [[],[1]]"],
"Every recursive call adds the current state to results (not just leaf nodes). This 'add then explore' pattern generates all 2^n subsets. The start index prevents duplicate subsets by only considering elements after the current position."))

problems.append((36,"Permutations","Medium","Backtracking",
"Given an array nums of distinct integers, return all possible permutations.",
["Input: [1,2,3]\nOutput: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"],
"Backtracking: swap each element with the current position, recurse, then swap back.",
"Time: O(n! × n) | Space: O(n!)",
"""function permutations(nums):
    result = []
    function backtrack(start):
        if start == len(nums): result.append(copy of nums); return
        for i in start..len(nums)-1:
            swap(nums[start], nums[i])
            backtrack(start+1)
            swap(nums[start], nums[i])
    backtrack(0)
    return result""",
"""import java.util.*;
public class Permutations {
    List<List<Integer>> res = new ArrayList<>();
    public List<List<Integer>> permute(int[] nums) {
        backtrack(nums, 0); return res;
    }
    void backtrack(int[] nums, int start) {
        if (start == nums.length) {
            List<Integer> perm = new ArrayList<>();
            for (int n : nums) perm.add(n);
            res.add(perm); return;
        }
        for (int i=start;i<nums.length;i++) {
            int tmp=nums[start]; nums[start]=nums[i]; nums[i]=tmp;
            backtrack(nums, start+1);
            tmp=nums[start]; nums[start]=nums[i]; nums[i]=tmp;
        }
    }
}""",
["[1,2,3] → 6 permutations","[1] → [[1]]","[1,2] → [[1,2],[2,1]]"],
"Swap-based permutation generation: at position i, try each remaining element by swapping it to position i, recurse for i+1, then undo the swap. Produces all n! permutations in-place without extra space for tracking 'used' elements."))

problems.append((37,"N-Queens","Hard","Backtracking",
"Place n queens on an n×n chessboard so that no two queens attack each other. Return all distinct solutions.",
["n=4 → 2 solutions: [['.Q..','...Q','Q...','..Q.'],['..Q.','Q...','...Q','.Q..']]"],
"Backtracking row by row. For each row, try placing queen in each column. Check column, diagonal, anti-diagonal constraints using sets.",
"Time: O(n!) | Space: O(n²)",
"""function solveNQueens(n):
    cols, diag1, diag2 = sets()
    board = ['.'*n for _ in range(n)]
    result = []
    function backtrack(row):
        if row == n: result.append(copy board); return
        for col in 0..n-1:
            if col in cols or (row-col) in diag1 or (row+col) in diag2: continue
            place queen; add to sets
            backtrack(row+1)
            remove queen; remove from sets
    backtrack(0); return result""",
"""import java.util.*;
public class NQueens {
    List<List<String>> res = new ArrayList<>();
    Set<Integer> cols=new HashSet<>(), d1=new HashSet<>(), d2=new HashSet<>();
    public List<List<String>> solveNQueens(int n) {
        char[][] b = new char[n][n];
        for (char[] r : b) Arrays.fill(r,'.');
        bt(b,0,n); return res;
    }
    void bt(char[][] b, int row, int n) {
        if (row==n){ List<String> sol=new ArrayList<>(); for(char[] r:b) sol.add(new String(r)); res.add(sol); return; }
        for (int c=0;c<n;c++) {
            if(cols.contains(c)||d1.contains(row-c)||d2.contains(row+c)) continue;
            b[row][c]='Q'; cols.add(c); d1.add(row-c); d2.add(row+c);
            bt(b,row+1,n);
            b[row][c]='.'; cols.remove(c); d1.remove(row-c); d2.remove(row+c);
        }
    }
}""",
["n=1 → 1 solution","n=2 → 0","n=4 → 2","n=8 → 92"],
"N-Queens is the canonical backtracking problem. Three sets (column, diagonal r-c, anti-diagonal r+c) give O(1) constraint checking. Diagonals are indexed by constant differences/sums — a beautiful mathematical insight."))

# ── SECTION 10: Heap / Priority Queue ────────────────────────────────────────
problems.append(("HEAP & PRIORITY QUEUE", None, None))

problems.append((38,"Top K Frequent Elements","Medium","Heap",
"Given an integer array nums and integer k, return the k most frequent elements.",
["Input: nums=[1,1,1,2,2,3], k=2 → [1,2]"],
"Count frequencies with a HashMap, then use a min-heap of size k. Or use bucket sort by frequency for O(n).",
"Time: O(n log k) heap, O(n) bucket | Space: O(n)",
"""function topKFrequent(nums, k):
    freq = frequency map of nums
    // Min-heap approach:
    heap = min-heap of size k on (count, num)
    for num, count in freq:
        heap.push((count, num))
        if heap.size > k: heap.pop()
    return elements of heap""",
"""import java.util.*;
public class TopKFrequent {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer,Integer> freq = new HashMap<>();
        for (int n : nums) freq.merge(n,1,Integer::sum);
        PriorityQueue<Integer> pq = new PriorityQueue<>((a,b)->freq.get(a)-freq.get(b));
        for (int n : freq.keySet()) {
            pq.offer(n);
            if (pq.size() > k) pq.poll();
        }
        int[] res = new int[k];
        for (int i=k-1;i>=0;i--) res[i]=pq.poll();
        return res;
    }
}""",
["[1,1,1,2,2,3],k=2 → [1,2]","[1],k=1 → [1]","[1,2],k=2 → [1,2]"],
"Min-heap of size k is the classic 'top k' pattern. The heap's minimum is always evicted when it exceeds size k, leaving exactly the k largest elements. This works for any 'top k' problem by frequency, value, or custom comparator."))

problems.append((39,"Find Median from Data Stream","Hard","Heap",
"Design a data structure that supports adding integers and finding the median in O(log n) add and O(1) find.",
["addNum(1), addNum(2), findMedian()→1.5, addNum(3), findMedian()→2.0"],
"Use two heaps: a max-heap for the lower half, a min-heap for the upper half. Keep sizes balanced (differ by at most 1).",
"Time: O(log n) add, O(1) median | Space: O(n)",
"""class MedianFinder:
    lo = max-heap  // lower half
    hi = min-heap  // upper half
    addNum(n):
        lo.push(n)
        hi.push(-lo.pop())  // balance
        if lo.size < hi.size: lo.push(-hi.pop())
    findMedian():
        if lo.size > hi.size: return lo.top
        return (lo.top - hi.top) / 2.0""",
"""import java.util.PriorityQueue;
public class MedianFinder {
    PriorityQueue<Integer> lo = new PriorityQueue<>((a,b)->b-a); // max-heap
    PriorityQueue<Integer> hi = new PriorityQueue<>();             // min-heap
    public void addNum(int n) {
        lo.offer(n);
        hi.offer(lo.poll());
        if (lo.size() < hi.size()) lo.offer(hi.poll());
    }
    public double findMedian() {
        return lo.size() > hi.size() ? lo.peek() : (lo.peek()+hi.peek())/2.0;
    }
}""",
["1,2,3 → medians: 1.0, 1.5, 2.0","Single element → that element","Two elements → average"],
"Two-heap approach maintains the invariant: all elements in lo ≤ all elements in hi, and their sizes differ by at most 1. The median is either the top of lo (odd count) or average of both tops (even count)."))

# ── SECTION 11: Tries ─────────────────────────────────────────────────────────
problems.append(("TRIE DATA STRUCTURE", None, None))

problems.append((40,"Implement Trie","Medium","Trie",
"Implement a Trie with insert, search, and startsWith operations.",
["Trie t; t.insert('apple'); t.search('apple')→true; t.search('app')→false; t.startsWith('app')→true"],
"Each node has an array of 26 children (one per letter) and a boolean isEnd flag. Insert/search follow the path character by character.",
"Time: O(L) per operation | Space: O(N×L) where N=words, L=avg length",
"""class TrieNode:
    children = [null]*26
    isEnd = false

class Trie:
    root = new TrieNode()
    insert(word):
        node = root
        for c in word:
            if not node.children[c-'a']: node.children[c-'a'] = new TrieNode()
            node = node.children[c-'a']
        node.isEnd = true
    search(word):
        node = traverse(word)
        return node != null and node.isEnd
    startsWith(prefix):
        return traverse(prefix) != null""",
"""public class Trie {
    class Node { Node[] ch = new Node[26]; boolean end; }
    Node root = new Node();
    public void insert(String w) {
        Node n=root; for(char c:w.toCharArray()){int i=c-'a';if(n.ch[i]==null)n.ch[i]=new Node();n=n.ch[i];} n.end=true;
    }
    public boolean search(String w) { Node n=find(w); return n!=null&&n.end; }
    public boolean startsWith(String p) { return find(p)!=null; }
    Node find(String s){Node n=root;for(char c:s.toCharArray()){int i=c-'a';if(n.ch[i]==null)return null;n=n.ch[i];}return n;}
}""",
["insert('apple'),search('apple')→true","search('app')→false","startsWith('app')→true","insert('app'),search('app')→true"],
"Trie (prefix tree) stores strings character by character. Lookup is O(L) regardless of how many strings are stored — far better than O(N) linear scan. Essential for autocomplete, spell checking, and IP routing."))

# ── SECTION 12: Advanced Graph ───────────────────────────────────────────────
problems.append(("ADVANCED GRAPH & SHORTEST PATH", None, None))

problems.append((41,"Network Delay Time (Dijkstra)","Medium","Dijkstra",
"There are n network nodes. Given times[i]=(u,v,w), find the time for all nodes to receive a signal sent from source k. Return -1 if impossible.",
["n=4, times=[[2,1,1],[2,3,1],[3,4,1]], k=2 → 2"],
"Dijkstra's algorithm with a min-heap. Start from k, greedily expand shortest known distances.",
"Time: O((V+E) log V) | Space: O(V+E)",
"""function networkDelayTime(times, n, k):
    graph = adjacency list from times
    dist = [INF]*n; dist[k]=0
    heap = [(0, k)]  // (dist, node)
    while heap:
        d, u = heap.pop_min()
        if d > dist[u]: continue
        for v, w in graph[u]:
            if dist[u]+w < dist[v]:
                dist[v] = dist[u]+w
                heap.push((dist[v], v))
    maxDist = max(dist[1..n])
    return maxDist if maxDist < INF else -1""",
"""import java.util.*;
public class NetworkDelay {
    public int networkDelayTime(int[][] times, int n, int k) {
        Map<Integer,List<int[]>> g = new HashMap<>();
        for (int[] t: times) g.computeIfAbsent(t[0],x->new ArrayList<>()).add(new int[]{t[1],t[2]});
        int[] dist = new int[n+1]; Arrays.fill(dist, Integer.MAX_VALUE); dist[k]=0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b)->a[0]-b[0]);
        pq.offer(new int[]{0,k});
        while (!pq.isEmpty()) {
            int[] cur=pq.poll(); int d=cur[0], u=cur[1];
            if (d>dist[u]) continue;
            if (!g.containsKey(u)) continue;
            for (int[] e:g.get(u)) if (dist[u]+e[1]<dist[e[0]]){dist[e[0]]=dist[u]+e[1];pq.offer(new int[]{dist[e[0]],e[0]});}
        }
        int ans=0; for(int i=1;i<=n;i++){if(dist[i]==Integer.MAX_VALUE)return -1;ans=Math.max(ans,dist[i]);}
        return ans;
    }
}""",
["[[2,1,1],[2,3,1],[3,4,1]],n=4,k=2 → 2","Unreachable node → -1","Single node → 0"],
"Dijkstra's algorithm: always expand the closest unvisited node. The min-heap ensures greedy correctness. Stale entries in the heap are discarded with the 'd > dist[u]' check — lazy deletion avoids a more complex decrease-key operation."))

problems.append((42,"Cheapest Flights Within K Stops (Bellman-Ford)","Medium","Bellman-Ford",
"Find the cheapest price from src to dst with at most k stops. Return -1 if impossible.",
["n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1 → 200"],
"Bellman-Ford variant: relax edges exactly k+1 times (k stops = k+1 edges). Use a copy of distances per iteration to prevent chaining in same round.",
"Time: O(K×E) | Space: O(V)",
"""function findCheapestPrice(n, flights, src, dst, k):
    prices = [INF]*n; prices[src]=0
    for i in 0..k:
        tmp = copy(prices)
        for u,v,w in flights:
            if prices[u] != INF and prices[u]+w < tmp[v]:
                tmp[v] = prices[u]+w
        prices = tmp
    return prices[dst] if prices[dst]!=INF else -1""",
"""import java.util.Arrays;
public class CheapestFlights {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] prices = new int[n]; Arrays.fill(prices, Integer.MAX_VALUE); prices[src]=0;
        for (int i=0;i<=k;i++) {
            int[] tmp = Arrays.copyOf(prices,n);
            for (int[] f: flights)
                if (prices[f[0]]!=Integer.MAX_VALUE && prices[f[0]]+f[2]<tmp[f[1]])
                    tmp[f[1]]=prices[f[0]]+f[2];
            prices=tmp;
        }
        return prices[dst]==Integer.MAX_VALUE ? -1 : prices[dst];
    }
}""",
["k=1,direct cheaper → direct","k=0,must go direct → direct price","No path → -1"],
"Bellman-Ford with exactly k+1 relaxation rounds enforces the 'at most k stops' constraint. The temporary copy is critical: using stale prices prevents a path from using more than one new edge per round."))

# ── SECTION 13: Union Find ────────────────────────────────────────────────────
problems.append(("UNION-FIND (DISJOINT SET)", None, None))

problems.append((43,"Number of Connected Components","Medium","Union-Find",
"Given n nodes and a list of edges, find the number of connected components in an undirected graph.",
["n=5, edges=[[0,1],[1,2],[3,4]] → 2"],
"Union-Find with path compression and union by rank. Count components by tracking how many unions actually merge different sets.",
"Time: O(α(n)) per operation | Space: O(n)",
"""class UnionFind:
    parent = [i for i in range(n)]
    rank = [0]*n
    count = n
    find(x): path compression with recursion
    union(x,y):
        px, py = find(x), find(y)
        if px == py: return
        merge by rank; count--""",
"""public class ConnectedComponents {
    int[] parent, rank;
    int count;
    ConnectedComponents(int n){ parent=new int[n]; rank=new int[n]; count=n; for(int i=0;i<n;i++) parent[i]=i; }
    int find(int x){ return parent[x]==x?x:(parent[x]=find(parent[x])); }
    void union(int a, int b){
        int pa=find(a),pb=find(b); if(pa==pb) return;
        if(rank[pa]<rank[pb]) parent[pa]=pb;
        else if(rank[pa]>rank[pb]) parent[pb]=pa;
        else { parent[pb]=pa; rank[pa]++; }
        count--;
    }
    public int countComponents(int n, int[][] edges) {
        for(int[] e:edges) union(e[0],e[1]);
        return count;
    }
}""",
["n=5, [[0,1],[1,2],[3,4]] → 2","n=5, no edges → 5","n=5, fully connected → 1"],
"Union-Find with path compression achieves near-O(1) per operation (amortised O(α(n)) where α is the inverse Ackermann function, effectively constant). Perfect for dynamic connectivity problems."))

# ── SECTION 14: Sorting Algorithms ───────────────────────────────────────────
problems.append(("SORTING ALGORITHMS", None, None))

problems.append((44,"Sort an Array (Merge Sort)","Medium","Sorting",
"Sort an array of integers using an efficient O(n log n) algorithm. Implement merge sort.",
["Input: [5,1,1,2,0,0] → [0,0,1,1,2,5]","Input: [5,2,3,1] → [1,2,3,5]"],
"Merge Sort: divide array in half recursively, then merge sorted halves. Classic divide-and-conquer.",
"Time: O(n log n) | Space: O(n)",
"""function mergeSort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr)//2
    left  = mergeSort(arr[:mid])
    right = mergeSort(arr[mid:])
    return merge(left, right)

function merge(l, r):
    result = []
    i = j = 0
    while i<len(l) and j<len(r):
        if l[i] <= r[j]: result.append(l[i++])
        else:             result.append(r[j++])
    return result + l[i:] + r[j:]""",
"""public class MergeSort {
    public int[] sortArray(int[] nums) { mergeSort(nums,0,nums.length-1); return nums; }
    void mergeSort(int[] a, int lo, int hi) {
        if (lo>=hi) return;
        int mid=lo+(hi-lo)/2;
        mergeSort(a,lo,mid); mergeSort(a,mid+1,hi); merge(a,lo,mid,hi);
    }
    void merge(int[] a, int lo, int mid, int hi) {
        int[] tmp = new int[hi-lo+1]; int i=lo,j=mid+1,k=0;
        while(i<=mid&&j<=hi) tmp[k++]=(a[i]<=a[j])?a[i++]:a[j++];
        while(i<=mid) tmp[k++]=a[i++]; while(j<=hi) tmp[k++]=a[j++];
        for(int x=0;x<tmp.length;x++) a[lo+x]=tmp[x];
    }
}""",
["[5,2,3,1] → [1,2,3,5]","[] → []","[1] → [1]","[2,1] → [1,2]"],
"Merge sort guarantees O(n log n) in all cases (unlike quicksort which degrades to O(n²) worst case). It's stable and the basis for TimSort (Java/Python's built-in sort). The merge step is the key: combining two sorted arrays is O(n)."))

problems.append((45,"Quick Sort","Medium","Sorting",
"Implement QuickSort. It's an in-place divide-and-conquer sorting algorithm.",
["Input: [3,6,8,10,1,2,1] → [1,1,2,3,6,8,10]"],
"Pick a pivot, partition array so smaller elements go left, larger go right, then recurse on both partitions.",
"Time: O(n log n) avg, O(n²) worst | Space: O(log n)",
"""function quickSort(arr, lo, hi):
    if lo < hi:
        pivot = partition(arr, lo, hi)
        quickSort(arr, lo, pivot-1)
        quickSort(arr, pivot+1, hi)

function partition(arr, lo, hi):
    pivot = arr[hi]
    i = lo-1
    for j in lo..hi-1:
        if arr[j] <= pivot:
            i++; swap(arr[i], arr[j])
    swap(arr[i+1], arr[hi])
    return i+1""",
"""public class QuickSort {
    public void quickSort(int[] a, int lo, int hi) {
        if (lo<hi){ int p=partition(a,lo,hi); quickSort(a,lo,p-1); quickSort(a,p+1,hi); }
    }
    int partition(int[] a, int lo, int hi) {
        int pivot=a[hi], i=lo-1;
        for(int j=lo;j<hi;j++) if(a[j]<=pivot){i++;int t=a[i];a[i]=a[j];a[j]=t;}
        int t=a[i+1];a[i+1]=a[hi];a[hi]=t; return i+1;
    }
}""",
["[3,6,8,10,1,2,1] → sorted","Already sorted (worst case for last-element pivot)","All same elements","Two elements"],
"QuickSort's average performance comes from good pivot selection. Median-of-three or randomised pivot avoids O(n²) worst case. In practice, QuickSort often outperforms MergeSort due to better cache locality and in-place operation."))

# ── SECTION 15: Advanced Topics ──────────────────────────────────────────────
problems.append(("ADVANCED DATA STRUCTURES & ALGORITHMS", None, None))

problems.append((46,"Segment Tree - Range Sum Query","Medium","Segment Tree",
"Design a data structure to support range sum queries and point updates on an array.",
["NumArray([1,3,5]); sumRange(0,2)→9; update(1,2); sumRange(0,2)→8"],
"Build a segment tree where each node stores sum of a range. Update and query in O(log n).",
"Time: O(n) build, O(log n) update/query | Space: O(n)",
"""class SegmentTree:
    tree = [0]*(4*n)
    build(arr, node, start, end):
        if start==end: tree[node]=arr[start]
        else:
            mid=(start+end)//2
            build(arr, 2*node, start, mid)
            build(arr, 2*node+1, mid+1, end)
            tree[node] = tree[2*node] + tree[2*node+1]
    query(node, start, end, l, r):
        if r<start or end<l: return 0
        if l<=start and end<=r: return tree[node]
        mid=(start+end)//2
        return query(2*node,start,mid,l,r) + query(2*node+1,mid+1,end,l,r)""",
"""public class NumArray {
    int[] tree; int n;
    public NumArray(int[] nums) {
        n=nums.length; tree=new int[4*n]; build(nums,1,0,n-1);
    }
    void build(int[] a, int node, int s, int e) {
        if(s==e){tree[node]=a[s];return;}
        int m=s+(e-s)/2; build(a,2*node,s,m); build(a,2*node+1,m+1,e);
        tree[node]=tree[2*node]+tree[2*node+1];
    }
    public void update(int i,int v){update(1,0,n-1,i,v);}
    void update(int node,int s,int e,int i,int v){
        if(s==e){tree[node]=v;return;}
        int m=s+(e-s)/2;
        if(i<=m)update(2*node,s,m,i,v); else update(2*node+1,m+1,e,i,v);
        tree[node]=tree[2*node]+tree[2*node+1];
    }
    public int sumRange(int l,int r){return query(1,0,n-1,l,r);}
    int query(int node,int s,int e,int l,int r){
        if(r<s||e<l)return 0; if(l<=s&&e<=r)return tree[node];
        int m=s+(e-s)/2; return query(2*node,s,m,l,r)+query(2*node+1,m+1,e,l,r);
    }
}""",
["sumRange(0,2)=9, update(1,2), sumRange(0,2)=8","Single element queries","Full range query"],
"Segment trees are the go-to for range queries with updates. Each node represents an interval; parent combines children. 4n space is sufficient. Lazy propagation extends this to range updates in O(log n)."))

problems.append((47,"Kruskal's MST Algorithm","Medium","Graph / MST",
"Find the Minimum Spanning Tree of a weighted undirected graph using Kruskal's algorithm.",
["edges=[(4,1,2),(8,2,3),(7,1,4),(9,3,4),(10,4,5)], n=5 → MST cost=28"],
"Sort edges by weight. Add edge if it doesn't create a cycle (use Union-Find to detect cycles).",
"Time: O(E log E) | Space: O(V)",
"""function kruskal(n, edges):
    sort edges by weight
    uf = UnionFind(n)
    mst_cost = 0
    for w, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_cost += w
    return mst_cost""",
"""import java.util.Arrays;
public class Kruskal {
    int[] parent, rank;
    int find(int x){ return parent[x]==x?x:(parent[x]=find(parent[x])); }
    boolean union(int a,int b){ int pa=find(a),pb=find(b); if(pa==pb) return false;
        if(rank[pa]<rank[pb]) parent[pa]=pb; else if(rank[pa]>rank[pb]) parent[pb]=pa;
        else{parent[pb]=pa;rank[pa]++;} return true; }
    public int minimumCost(int n, int[][] conns) {
        parent=new int[n+1]; rank=new int[n+1]; for(int i=0;i<=n;i++) parent[i]=i;
        Arrays.sort(conns,(a,b)->a[2]-b[2]); int cost=0,edges=0;
        for(int[] c:conns){ if(union(c[0],c[1])){cost+=c[2];if(++edges==n-1) break;} }
        return edges==n-1?cost:-1;
    }
}""",
["Connected graph → MST cost","Disconnected → -1","Single node → 0"],
"Kruskal's greedy proof: adding the minimum weight edge that doesn't form a cycle always leads to an MST. Union-Find makes cycle detection O(α(n)). Alternative: Prim's algorithm works better on dense graphs."))

problems.append((48,"Topological Sort (Kahn's BFS)","Medium","Graph",
"Given a directed acyclic graph, return a valid topological ordering of vertices.",
["n=6, edges=[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]] → [4,5,0,2,3,1]"],
"Kahn's BFS: compute in-degrees, start with 0-in-degree nodes, BFS processing removes edges and reduces in-degrees.",
"Time: O(V+E) | Space: O(V+E)",
"""function topoSort(n, edges):
    graph = adjacency list
    inDegree = [0]*n
    for u,v in edges: graph[u].add(v); inDegree[v]++
    q = Queue of nodes with inDegree==0
    order = []
    while q not empty:
        node = q.dequeue(); order.append(node)
        for nb in graph[node]:
            inDegree[nb]--
            if inDegree[nb]==0: q.enqueue(nb)
    return order if len(order)==n else []  // empty if cycle""",
"""import java.util.*;
public class TopologicalSort {
    public int[] findOrder(int n, int[][] prereqs) {
        List<List<Integer>> g=new ArrayList<>(); int[] ind=new int[n];
        for(int i=0;i<n;i++) g.add(new ArrayList<>());
        for(int[] p:prereqs){g.get(p[1]).add(p[0]);ind[p[0]]++;}
        Queue<Integer> q=new LinkedList<>();
        for(int i=0;i<n;i++) if(ind[i]==0) q.offer(i);
        int[] res=new int[n]; int idx=0;
        while(!q.isEmpty()){int u=q.poll();res[idx++]=u;for(int v:g.get(u)) if(--ind[v]==0) q.offer(v);}
        return idx==n?res:new int[0];
    }
}""",
["DAG → valid ordering","Graph with cycle → empty","Single node → [0]"],
"Kahn's algorithm detects cycles too: if the output has fewer than n nodes, a cycle exists (those nodes never reach in-degree 0). BFS gives topological order naturally since we always process 'ready' nodes first."))

problems.append((49,"Longest Increasing Subsequence","Medium","DP / Binary Search",
"Given integer array nums, return the length of the longest strictly increasing subsequence.",
["Input: [10,9,2,5,3,7,101,18] → 4 ([2,3,7,101])"],
"O(n log n) patience sorting approach: maintain a 'tails' array. Binary search to find position for each element.",
"Time: O(n log n) | Space: O(n)",
"""function LIS(nums):
    tails = []
    for n in nums:
        pos = binary_search(tails, n)  // leftmost pos where tails[pos] >= n
        if pos == len(tails): tails.append(n)
        else: tails[pos] = n
    return len(tails)""",
"""import java.util.Arrays;
public class LIS {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length]; int size=0;
        for (int n : nums) {
            int lo=0,hi=size;
            while(lo<hi){int mid=lo+(hi-lo)/2;if(tails[mid]<n)lo=mid+1;else hi=mid;}
            tails[lo]=n; if(lo==size) size++;
        }
        return size;
    }
}""",
["[10,9,2,5,3,7,101,18] → 4","[0,1,0,3,2,3] → 4","[7,7,7,7] → 1","[1,3,6,7,9,4,10,5,6] → 6"],
"The patience sorting insight: 'tails[i]' is the smallest tail element of all increasing subsequences of length i+1. Binary search finds the right pile. tails is never the actual LIS, but its length equals the LIS length."))

problems.append((50,"Serialize and Deserialize Binary Tree","Hard","Trees / Design",
"Design an algorithm to serialize a binary tree to a string and deserialize it back to the tree.",
["Tree: 1→(2,3→(4,5)) serializes to '1,2,null,null,3,4,null,null,5,null,null'"],
"Pre-order DFS serialization. Use 'null' for missing nodes. Deserialization consumes the string node by node.",
"Time: O(n) | Space: O(n)",
"""function serialize(root):
    if root == null: return 'null,'
    return str(root.val)+',' + serialize(root.left) + serialize(root.right)

function deserialize(data):
    queue = data.split(',')
    function dfs():
        val = queue.dequeue()
        if val == 'null': return null
        node = new TreeNode(int(val))
        node.left  = dfs()
        node.right = dfs()
        return node
    return dfs()""",
"""import java.util.*;
public class Codec {
    public String serialize(TreeNode root) {
        if(root==null) return "null,";
        return root.val+","+serialize(root.left)+serialize(root.right);
    }
    Queue<String> q;
    public TreeNode deserialize(String data) {
        q=new LinkedList<>(Arrays.asList(data.split(",")));
        return dfs();
    }
    TreeNode dfs(){ String v=q.poll(); if(v.equals("null")) return null;
        TreeNode n=new TreeNode(Integer.parseInt(v)); n.left=dfs(); n.right=dfs(); return n; }
}""",
["Any binary tree round-trips correctly","null → null","Single node → '1,null,null'","Complete tree"],
"Pre-order serialization is self-describing: the position of 'null' markers fully encodes the tree structure. Alternatively, level-order BFS serialization is more human-readable but uses the same concept."))

# ── additional problems 51-100 ─────────────────────────────────────────────────

extras = [
(51,"Spiral Matrix","Medium","Arrays","Return all elements of an m×n matrix in spiral order.",
["[[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]"],
"Peel layers: traverse top row, right col, bottom row, left col, then shrink boundaries.",
"Time: O(m×n) | Space: O(1) extra",
"top,bot,left,right boundaries\nwhile top<=bot and left<=right:\n  traverse top; top++\n  traverse right; right--\n  traverse bottom if top<=bot; bot--\n  traverse left if left<=right; left++",
"public List<Integer> spiralOrder(int[][] m){\n  List<Integer> r=new ArrayList<>();int t=0,b=m.length-1,l=0,ri=m[0].length-1;\n  while(t<=b&&l<=ri){for(int i=l;i<=ri;i++)r.add(m[t][i]);t++;\n  for(int i=t;i<=b;i++)r.add(m[i][ri]);ri--;\n  if(t<=b){for(int i=ri;i>=l;i--)r.add(m[b][i]);b--;}\n  if(l<=ri){for(int i=b;i>=t;i--)r.add(m[i][l]);l++;}}\n  return r;\n}",
["3x3 → 9 elements in order","1 row → that row","1 col → that col"],
"Boundary-shrinking spiral: four boundary variables track remaining area. Each full loop shrinks by one layer."),

(52,"Rotate Image","Medium","Arrays","Rotate an n×n matrix 90° clockwise in-place.",
["[[1,2,3],[4,5,6],[7,8,9]] → [[7,4,1],[8,5,2],[9,6,3]]"],
"Transpose (flip along main diagonal), then reverse each row.",
"Time: O(n²) | Space: O(1)",
"// transpose\nfor i: for j>i: swap(m[i][j], m[j][i])\n// reverse each row\nfor each row: reverse(row)",
"public void rotate(int[][] m){\n  int n=m.length;\n  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){int t=m[i][j];m[i][j]=m[j][i];m[j][i]=t;}\n  for(int[] row:m){int l=0,r=n-1;while(l<r){int t=row[l];row[l]=row[r];row[r]=t;l++;r--;}}\n}",
["1×1 → unchanged","2×2 → rotated","4×4 stress test"],
"Transpose + reverse = 90° CW rotation. This in-place insight avoids an extra O(n²) matrix and generalises to other rotation angles."),

(53,"Set Matrix Zeroes","Medium","Arrays","If an element is 0, set its entire row and column to 0 (in-place).",
["[[1,1,1],[1,0,1],[1,1,1]] → [[1,0,1],[0,0,0],[1,0,1]]"],
"Use first row and first column as markers. Scan rest of matrix, mark zeros in headers, then apply.",
"Time: O(m×n) | Space: O(1)",
"record if first row/col have zeros\nfor i,j in matrix[1:][1:]:\n  if matrix[i][j]==0: matrix[i][0]=matrix[0][j]=0\napply markers\nhandle first row/col",
"public void setZeroes(int[][] m){\n  boolean fr=false,fc=false;\n  for(int j=0;j<m[0].length;j++) if(m[0][j]==0) fr=true;\n  for(int i=0;i<m.length;i++) if(m[i][0]==0) fc=true;\n  for(int i=1;i<m.length;i++) for(int j=1;j<m[0].length;j++) if(m[i][j]==0){m[i][0]=0;m[0][j]=0;}\n  for(int i=1;i<m.length;i++) for(int j=1;j<m[0].length;j++) if(m[i][0]==0||m[0][j]==0) m[i][j]=0;\n  if(fr) Arrays.fill(m[0],0); if(fc) for(int[] r:m) r[0]=0;\n}",
["No zeros → unchanged","All zeros → all zeros","Single zero"],
"Using the matrix's own borders as flags achieves O(1) extra space. The 'first row/col' special case handling is the tricky part."),

(54,"Jump Game","Medium","Greedy","Given array nums where nums[i] is max jump from i, return true if you can reach the last index.",
["[2,3,1,1,4] → true","[3,2,1,0,4] → false"],
"Greedy: track maximum reachable index. If current index > maxReach, return false.",
"Time: O(n) | Space: O(1)",
"maxReach = 0\nfor i,n in enumerate(nums):\n  if i > maxReach: return false\n  maxReach = max(maxReach, i+n)\nreturn true",
"public boolean canJump(int[] n){\n  int max=0;\n  for(int i=0;i<n.length;i++){\n    if(i>max) return false;\n    max=Math.max(max,i+n[i]);\n  }\n  return true;\n}",
["[2,3,1,1,4] → true","[3,2,1,0,4] → false","[0] → true","[1,0] → true"],
"Greedy maximum-reach: we only need to know the farthest reachable index at each point. If our current index exceeds it, we're stuck."),

(55,"Gas Station","Medium","Greedy","Find the starting gas station index for a circular route, or -1 if impossible.",
["gas=[1,2,3,4,5], cost=[3,4,5,1,2] → 3"],
"If total gas >= total cost, a solution exists. Start where tank doesn't go negative.",
"Time: O(n) | Space: O(1)",
"total=0, tank=0, start=0\nfor i:\n  diff=gas[i]-cost[i]\n  tank+=diff; total+=diff\n  if tank<0: start=i+1; tank=0\nreturn start if total>=0 else -1",
"public int canCompleteCircuit(int[] g, int[] c){\n  int total=0,tank=0,start=0;\n  for(int i=0;i<g.length;i++){\n    int d=g[i]-c[i]; total+=d; tank+=d;\n    if(tank<0){start=i+1;tank=0;}\n  }\n  return total>=0?start:-1;\n}",
["gas=[1,2,3,4,5],cost=[3,4,5,1,2] → 3","Impossible → -1","Single station: gas>=cost → 0"],
"If sum(gas)>=sum(cost), a unique solution always exists. The start is reset whenever the tank goes negative, as all earlier stations are insufficient starting points."),

(56,"Trapping Rain Water","Hard","Two Pointers","Compute how much water can be trapped between bars.",
["[0,1,0,2,1,0,1,3,2,1,2,1] → 6"],
"Two-pointer approach: track left_max and right_max. Water at each position = min(left_max, right_max) - height.",
"Time: O(n) | Space: O(1)",
"l,r=0,n-1; lmax=rmax=0; water=0\nwhile l<r:\n  if height[l]<height[r]:\n    if height[l]>=lmax: lmax=height[l]\n    else: water+=lmax-height[l]\n    l++\n  else: symmetric for r",
"public int trap(int[] h){\n  int l=0,r=h.length-1,lm=0,rm=0,w=0;\n  while(l<r){\n    if(h[l]<h[r]){if(h[l]>=lm)lm=h[l];else w+=lm-h[l];l++;}\n    else{if(h[r]>=rm)rm=h[r];else w+=rm-h[r];r--;}\n  }\n  return w;\n}",
["Flat → 0","V-shape → trapped","All increasing → 0"],
"The two-pointer insight: water at position i is bounded by the minimum of max-left and max-right. Moving from the smaller side guarantees we know the limiting factor."),

(57,"Container With Most Water","Medium","Two Pointers","Find two lines forming a container with maximum water.",
["[1,8,6,2,5,4,8,3,7] → 49"],
"Two pointers from ends. Move the shorter pointer inward (only moving the taller pointer can never improve area).",
"Time: O(n) | Space: O(1)",
"l,r=0,n-1; maxWater=0\nwhile l<r:\n  maxWater=max(maxWater, min(h[l],h[r])*(r-l))\n  if h[l]<h[r]: l++ else r--",
"public int maxArea(int[] h){\n  int l=0,r=h.length-1,max=0;\n  while(l<r){\n    max=Math.max(max,Math.min(h[l],h[r])*(r-l));\n    if(h[l]<h[r])l++;else r--;\n  }\n  return max;\n}",
["[1,1] → 1","All same height → n-1","Increasing → last two elements"],
"Width decreases as we move inward, so we must increase height. Moving the taller side can never help (limited by shorter). Only by moving the shorter side might we find a taller wall that compensates."),

(58,"Longest Palindromic Substring","Medium","DP / Expand Around Center","Find the longest palindromic substring.",
["'babad' → 'bab' or 'aba'","'cbbd' → 'bb'"],
"Expand around center for each position. Check both odd and even length palindromes.",
"Time: O(n²) | Space: O(1)",
"for each center (2n-1 centers for odd+even):\n  expand while chars match\n  track longest",
"public String longestPalindrome(String s){\n  String res=\"\";\n  for(int i=0;i<s.length();i++){\n    String odd=expand(s,i,i), even=expand(s,i,i+1);\n    if(odd.length()>res.length())res=odd;\n    if(even.length()>res.length())res=even;\n  }\n  return res;\n}\nString expand(String s,int l,int r){\n  while(l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r)){l--;r++;}\n  return s.substring(l+1,r);\n}",
["Single char → itself","All same → whole string","'a' → 'a'"],
"Expanding around center is simpler than DP and uses O(1) space. Manacher's algorithm achieves O(n) but is complex to implement."),

(59,"Decode Ways","Medium","DP","Count ways to decode a digit string to letters (1='A'..26='Z').",
["'12' → 2 ('AB' or 'L')","'226' → 3","'06' → 0"],
"DP where dp[i] = ways to decode s[0..i-1]. Single digit valid if 1-9; double digit valid if 10-26.",
"Time: O(n) | Space: O(n)",
"dp[0]=1; dp[1]=1 if s[0]!='0' else 0\nfor i in 2..n:\n  one = int(s[i-1])\n  two = int(s[i-2:i])\n  if one>=1: dp[i]+=dp[i-1]\n  if 10<=two<=26: dp[i]+=dp[i-2]",
"public int numDecodings(String s){\n  int n=s.length(); int[]dp=new int[n+1];\n  dp[0]=1; dp[1]=s.charAt(0)=='0'?0:1;\n  for(int i=2;i<=n;i++){\n    int one=s.charAt(i-1)-'0', two=Integer.parseInt(s.substring(i-2,i));\n    if(one>=1)dp[i]+=dp[i-1];\n    if(two>=10&&two<=26)dp[i]+=dp[i-2];\n  }\n  return dp[n];\n}",
["'12' → 2","'226' → 3","'0' → 0","'10' → 1"],
"Decode Ways is a Fibonacci-like DP. Each position depends on the previous one or two digits. The boundary checks (no leading zeros, two-digit range 10-26) are critical for correctness."),

(60,"House Robber","Medium","DP","Rob non-adjacent houses to maximise total.",
["[1,2,3,1] → 4","[2,7,9,3,1] → 12"],
"DP: rob[i] = max(rob[i-1], rob[i-2]+nums[i]). Optimise to O(1) space with two variables.",
"Time: O(n) | Space: O(1)",
"prev2, prev1 = 0, 0\nfor n in nums:\n  cur = max(prev1, prev2+n)\n  prev2=prev1; prev1=cur\nreturn prev1",
"public int rob(int[] n){\n  int p2=0,p1=0;\n  for(int x:n){int c=Math.max(p1,p2+x);p2=p1;p1=c;}\n  return p1;\n}",
["[1,2,3,1] → 4","[2,7,9,3,1] → 12","[1] → 1","[2,1] → 2"],
"Classic DP with rolling window. The decision tree: rob this house (add to grandparent's result) or skip (take parent's result). Optimising to O(1) space by recognising we only look back 2 steps."),
]

for e in extras:
    problems.append(e)

# add 40 more concise problems
short_probs = [
(61,"Palindrome Number","Easy","Math","Determine if integer is palindrome without string conversion.",["121→true","-121→false"],"Reverse second half, compare with first half.","O(log n) time | O(1) space","reverse second half of digits, compare","public boolean isPalindrome(int x){if(x<0||(x!=0&&x%10==0))return false;int r=0;while(x>r){r=r*10+x%10;x/=10;}return x==r||x==r/10;}",["121→true","1221→true","-121→false","10→false"],"No string needed: reverse only half the digits."),
(62,"Roman to Integer","Easy","String","Convert Roman numeral string to integer.",["'III'→3","'IX'→9","'MCMXCIV'→1994"],"Map each symbol. If current < next, subtract; otherwise add.","O(n) time | O(1) space","map={I:1,V:5,X:10,L:50,C:100,D:500,M:1000}\nfor i: if map[s[i]]<map[s[i+1]]: result-=map[s[i]] else result+=map[s[i]]","public int romanToInt(String s){Map<Character,Integer>m=new HashMap<>();m.put('I',1);m.put('V',5);m.put('X',10);m.put('L',50);m.put('C',100);m.put('D',500);m.put('M',1000);int r=0;for(int i=0;i<s.length();i++){int v=m.get(s.charAt(i));if(i+1<s.length()&&v<m.get(s.charAt(i+1)))r-=v;else r+=v;}return r;}",["'III'→3","'IX'→9","'MCMXCIV'→1994"],"Roman numeral's subtraction rule triggers when a smaller value precedes a larger one."),
(63,"Fizz Buzz","Easy","Math","For 1..n, print Fizz(÷3), Buzz(÷5), FizzBuzz(÷15), or number.",["n=5→['1','2','Fizz','4','Buzz']"],"Check divisibility in order: 15 first, then 3, then 5.","O(n) time | O(n) space","for i 1..n: if i%15==0: FizzBuzz elif i%3==0: Fizz elif i%5==0: Buzz else str(i)","public List<String> fizzBuzz(int n){List<String>r=new ArrayList<>();for(int i=1;i<=n;i++){if(i%15==0)r.add(\"FizzBuzz\");else if(i%3==0)r.add(\"Fizz\");else if(i%5==0)r.add(\"Buzz\");else r.add(String.valueOf(i));}return r;}",["n=3→['1','2','Fizz']","n=15→FizzBuzz at 15"],"Check 15 before 3 and 5 to avoid partial matches. FizzBuzz tests understanding of modular arithmetic."),
(64,"Count Primes","Medium","Math","Count primes less than n using Sieve of Eratosthenes.",["n=10→4 (2,3,5,7)"],"Sieve: mark multiples of each prime as composite.","O(n log log n) time | O(n) space","sieve=bool[n] init True\nfor p from 2 to sqrt(n):\n  if sieve[p]: mark p*p,p*p+p,... as False\ncount True values","public int countPrimes(int n){boolean[]s=new boolean[n];Arrays.fill(s,true);for(int i=2;(long)i*i<n;i++)if(s[i])for(int j=i*i;j<n;j+=i)s[j]=false;int c=0;for(int i=2;i<n;i++)if(s[i])c++;return c;}",["n=10→4","n=1→0","n=2→0","n=3→1"],"Sieve of Eratosthenes: start marking from p² (smaller multiples already marked). Most efficient known algorithm for bulk prime finding."),
(65,"Power of Two","Easy","Bit Manipulation","Check if n is a power of two.",["n=1→true","n=16→true","n=3→false"],"n>0 and n&(n-1)==0: powers of two have exactly one set bit.","O(1) time | O(1) space","return n>0 and (n & (n-1))==0","public boolean isPowerOfTwo(int n){return n>0&&(n&(n-1))==0;}",["1→true","16→true","3→false","0→false"],"n&(n-1) clears the lowest set bit. If the result is 0, n had exactly one set bit → power of two."),
(66,"Reverse Bits","Easy","Bit Manipulation","Reverse bits of a 32-bit unsigned integer.",["00000010100101000001111010011100 → reversed"],"Loop 32 times: shift result left, OR with LSB of n, shift n right.","O(1) time | O(1) space","result=0\nfor _ in range(32): result=(result<<1)|(n&1); n>>=1","public int reverseBits(int n){int r=0;for(int i=0;i<32;i++){r=(r<<1)|(n&1);n>>=1;}return r;}",["43261596 → 964176192","0 → 0","4294967293 → flipped"],"Bit reversal: extract LSB each round, append to result. 32 iterations regardless of input."),
(67,"Number of 1 Bits","Easy","Bit Manipulation","Return count of 1 bits in integer (Hamming weight).",["n=11 (binary 1011) → 3"],"Brian Kernighan: n&(n-1) removes lowest set bit. Count iterations until 0.","O(k) where k=set bits | O(1) space","count=0\nwhile n!=0: n=n&(n-1); count++","public int hammingWeight(int n){int c=0;while(n!=0){n&=(n-1);c++;}return c;}",["11→3","128→1","0→0"],"n&(n-1) is a classic trick to clear the lowest set bit. Faster than checking each bit when the number is sparse."),
(68,"Excel Sheet Column Number","Easy","Math","Convert Excel column title ('A','B'...,'Z','AA'...) to column number.",["'A'→1","'AB'→28","'ZY'→701"],"Process as base-26 number: result = result*26 + (char-'A'+1).","O(n) time | O(1) space","result=0\nfor c in title: result=result*26+(c-'A'+1)","public int titleToNumber(String t){int r=0;for(char c:t.toCharArray())r=r*26+(c-'A'+1);return r;}",["'A'→1","'Z'→26","'AA'→27","'ZY'→701"],"Excel columns are base-26 with no zero digit (A=1..Z=26,AA=27). Horner's method evaluates the polynomial efficiently."),
(69,"Missing Number","Easy","Bit Manipulation / Math","Find missing number in array containing 0 to n.",["[3,0,1] → 2","[9,6,4,2,3,5,7,0,1] → 8"],"Expected sum = n*(n+1)/2. Subtract actual sum. Or XOR approach.","O(n) time | O(1) space","return n*(n+1)/2 - sum(nums)","public int missingNumber(int[] n){int s=n.length*(n.length+1)/2;for(int x:n)s-=x;return s;}",["[3,0,1]→2","[0,1]→2","[1]→0","[0]→1"],"Gauss's formula gives expected sum in O(1). XOR alternative: XOR all indices and values — duplicates cancel, leaving the missing number."),
(70,"Reverse String","Easy","Two Pointers","Reverse a character array in-place.",["['h','e','l','l','o'] → ['o','l','l','e','h']"],"Two pointer swap from both ends inward.","O(n) time | O(1) space","l,r=0,len-1\nwhile l<r: swap(s[l],s[r]); l++; r--","public void reverseString(char[] s){int l=0,r=s.length-1;while(l<r){char t=s[l];s[l]=s[r];s[r]=t;l++;r--;}}",["['h','e','l','l','o']→['o','l','l','e','h']","single char → unchanged","even length"],"In-place reversal with two pointers is O(1) extra space. This is the foundation for anagram checks, palindrome verification, and many string manipulation algorithms."),
(71,"First Bad Version","Easy","Binary Search","Find first bad version given an API isBadVersion(version).",["n=5, bad=4 → 4"],"Binary search: if mid is bad, search left half; else search right half.","O(log n) time | O(1) space","lo,hi=1,n\nwhile lo<hi: mid=(lo+hi)//2\n  if isBadVersion(mid): hi=mid\n  else: lo=mid+1\nreturn lo","public int firstBadVersion(int n){int lo=1,hi=n;while(lo<hi){int mid=lo+(hi-lo)/2;if(isBadVersion(mid))hi=mid;else lo=mid+1;}return lo;}",["bad=4,n=5→4","bad=1→1","bad=n→n"],"Classic binary search variant: find leftmost condition. Use hi=mid (not mid-1) because mid might be the answer. The lo+(hi-lo)/2 avoids overflow."),
(72,"Sqrt(x)","Easy","Binary Search","Compute integer square root of x without using sqrt().","[x=4→2, x=8→2]","Binary search 1..x for largest k where k²≤x.","O(log x) time | O(1) space","lo,hi=1,x\nwhile lo<=hi: mid=(lo+hi)//2\n  if mid*mid==x: return mid\n  elif mid*mid<x: lo=mid+1; ans=mid\n  else: hi=mid-1\nreturn ans","public int mySqrt(int x){if(x<2)return x;int lo=1,hi=x/2,ans=0;while(lo<=hi){int mid=lo+(hi-lo)/2;if((long)mid*mid==x)return mid;else if((long)mid*mid<x){ans=mid;lo=mid+1;}else hi=mid-1;}return ans;}",["4→2","8→2","1→1","0→0"],"Binary search on answer space. Cast to long to prevent mid*mid overflow for large x."),
(73,"Pascal's Triangle","Easy","DP","Generate first numRows rows of Pascal's triangle.",["numRows=5 → [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"],"Each row: edge elements are 1, interior = sum of two elements from row above.","O(n²) time | O(n²) space","res=[[1]]\nfor i in 1..n-1:\n  row=[1]\n  for j in 1..i-1: row.append(prev[j-1]+prev[j])\n  row.append(1); res.append(row)","public List<List<Integer>> generate(int n){List<List<Integer>>r=new ArrayList<>();for(int i=0;i<n;i++){List<Integer>row=new ArrayList<>();for(int j=0;j<=i;j++)row.add(j==0||j==i?1:r.get(i-1).get(j-1)+r.get(i-1).get(j));r.add(row);}return r;}",["n=1→[[1]]","n=5→correct triangle"],"Pascal's triangle encodes combinatorial coefficients C(n,k). Row n sums to 2^n. Diagonal gives triangular numbers, powers of 2, Fibonacci numbers."),
(74,"Search a 2D Matrix","Medium","Binary Search","Each row sorted, first element of each row > last element of previous row. Search for target.","[[[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3 → true]","Treat as flattened sorted array, binary search with 2D index mapping.","O(log(m×n)) time | O(1) space","lo=0,hi=m*n-1\nwhile lo<=hi: mid=(lo+hi)//2; val=m[mid//n][mid%n]\n  compare val with target","public boolean searchMatrix(int[][] m,int t){int r=m.length,c=m[0].length,lo=0,hi=r*c-1;while(lo<=hi){int mid=lo+(hi-lo)/2,v=m[mid/c][mid%c];if(v==t)return true;else if(v<t)lo=mid+1;else hi=mid-1;}return false;}",["target found → true","target not found → false","1×1 matrix"],"Flattening a 2D sorted matrix to 1D binary search: row = index/cols, col = index%cols. Elegant O(log mn) solution."),
(75,"Kth Largest Element","Medium","Heap / QuickSelect","Find kth largest element in unsorted array.",["[3,2,1,5,6,4], k=2 → 5"],"Min-heap of size k: maintain k largest elements. Or QuickSelect for O(n) average.","O(n log k) heap | O(n) QuickSelect average","min-heap of size k\nfor n in nums: heap.push(n); if size>k: heap.pop()","public int findKthLargest(int[] n,int k){PriorityQueue<Integer>pq=new PriorityQueue<>();for(int x:n){pq.offer(x);if(pq.size()>k)pq.poll();}return pq.peek();}",["[3,2,1,5,6,4],k=2→5","[1],k=1→1","all same,k=1→that value"],"Min-heap of size k keeps k largest. Top is kth largest. QuickSelect (partial quicksort) gives O(n) average but O(n²) worst case."),
(76,"Group Anagrams","Medium","HashMap","Group strings that are anagrams of each other.",["['eat','tea','tan','ate','nat','bat'] → [['eat','tea','ate'],['tan','nat'],['bat']]"],"Sort each word as key in HashMap. Group by same key.","O(n×k log k) where k=max word length | O(n×k) space","map: sorted_word → [words]\nfor w in strs: map[sort(w)].append(w)","public List<List<String>> groupAnagrams(String[] s){Map<String,List<String>>m=new HashMap<>();for(String w:s){char[]c=w.toCharArray();Arrays.sort(c);m.computeIfAbsent(new String(c),k->new ArrayList<>()).add(w);}return new ArrayList<>(m.values());}",["['eat','tea','ate'] grouped","All unique → each alone","All same → one group"],"Sorted string as canonical form: anagrams produce identical sorted strings. Frequency array of 26 chars as key avoids sorting."),
(77,"Longest Consecutive Sequence","Medium","HashSet","Find length of longest consecutive sequence in unsorted array (O(n) time).",["[100,4,200,1,3,2] → 4 (1,2,3,4)"],"HashSet for O(1) lookup. Start sequence only from sequence beginnings (n-1 not in set). Extend and count.","O(n) time | O(n) space","set=HashSet(nums)\nfor n in nums:\n  if n-1 not in set:  // start of sequence\n    cur=n; length=1\n    while cur+1 in set: cur++; length++\n    maxLen=max(maxLen,length)","public int longestConsecutive(int[] n){Set<Integer>s=new HashSet<>();for(int x:n)s.add(x);int max=0;for(int x:n)if(!s.contains(x-1)){int c=x,l=1;while(s.contains(c+1)){c++;l++;}max=Math.max(max,l);}return max;}",["[100,4,200,1,3,2]→4","[0,3,7,2,5,8,4,6,0,1]→9","[]→0"],"Only start counting from sequence beginnings (no predecessor in set). This ensures each sequence is counted once and total work is O(n)."),
(78,"Find All Duplicates","Medium","Arrays","Find all integers that appear twice in array [1..n] (in-place O(1) space).",["[4,3,2,7,8,2,3,1] → [2,3]"],"Negate element at index corresponding to each value. If already negative, it's a duplicate.","O(n) time | O(1) extra space","for each num n:\n  idx=abs(n)-1\n  if nums[idx]<0: result.add(abs(n))\n  else: nums[idx]=-nums[idx]","public List<Integer> findDuplicates(int[] n){List<Integer>r=new ArrayList<>();for(int x:n){int i=Math.abs(x)-1;if(n[i]<0)r.add(Math.abs(x));else n[i]=-n[i];}return r;}",["[4,3,2,7,8,2,3,1]→[2,3]","No duplicates → []","All duplicates → all"],"Using the array itself as a frequency marker: map value v to index v-1, toggle sign. Second visit to same index reveals duplicate."),
(79,"Sort Colors","Medium","Two Pointers","Sort array containing 0s, 1s, 2s in-place (Dutch National Flag).",["[2,0,2,1,1,0] → [0,0,1,1,2,2]"],"Three pointers: low(0s boundary), mid(current), high(2s boundary). One pass.","O(n) time | O(1) space","lo=0,mid=0,hi=n-1\nwhile mid<=hi:\n  if arr[mid]==0: swap(lo,mid);lo++;mid++\n  elif arr[mid]==1: mid++\n  else: swap(mid,hi);hi--","public void sortColors(int[] n){int lo=0,mid=0,hi=n.length-1;while(mid<=hi){if(n[mid]==0){int t=n[lo];n[lo]=n[mid];n[mid]=t;lo++;mid++;}else if(n[mid]==1)mid++;else{int t=n[mid];n[mid]=n[hi];n[hi]=t;hi--;}}}",["[2,0,2,1,1,0]→[0,0,1,1,2,2]","All 0s","All same color","Two 2s, no 1s"],"Dijkstra's Dutch National Flag: maintain three regions. When we see 0, expand the 0-region; when 2, expand the 2-region. 1s fall naturally in between."),
(80,"Majority Element","Easy","Boyer-Moore","Find element appearing more than n/2 times.",["[3,2,3] → 3","[2,2,1,1,1,2,2] → 2"],"Boyer-Moore voting: maintain candidate and count. Count drops to 0 → new candidate.","O(n) time | O(1) space","candidate=nums[0], count=1\nfor n in nums[1:]:\n  if count==0: candidate=n; count=1\n  elif n==candidate: count++\n  else: count--\nreturn candidate","public int majorityElement(int[] n){int c=n[0],cnt=1;for(int i=1;i<n.length;i++){if(cnt==0){c=n[i];cnt=1;}else if(n[i]==c)cnt++;else cnt--;}return c;}",["[3,2,3]→3","[2,2,1,1,1,2,2]→2","Single element → itself"],"Boyer-Moore voting: the majority element 'survives' because it appears more than all others combined. When a non-majority element cancels a vote, the majority still has remaining votes."),
(81,"Move Zeroes","Easy","Two Pointers","Move all zeroes to end while maintaining relative order of non-zero elements.",["[0,1,0,3,12] → [1,3,12,0,0]"],"Two pointers: left points to next zero position. Copy non-zeros forward, then fill rest with zeros.","O(n) time | O(1) space","pos=0\nfor n in nums: if n!=0: nums[pos]=n; pos++\nfill nums[pos..] with 0","public void moveZeroes(int[] n){int p=0;for(int x:n)if(x!=0)n[p++]=x;while(p<n.length)n[p++]=0;}",["[0,1,0,3,12]→[1,3,12,0,0]","No zeros → unchanged","All zeros → all zeros"],"Two-pointer partition: compact all non-zeros to the front, then fill the tail with zeros. Preserves relative order of non-zero elements."),
(82,"Intersection of Two Arrays II","Easy","HashMap","Return intersection of two arrays with duplicates.",["[1,2,2,1],[2,2] → [2,2]"],"Count frequencies with map. For each element in second array, check if count>0 in map.","O(m+n) time | O(min(m,n)) space","map=freq count of nums1\nfor n in nums2: if map[n]>0: result.add(n); map[n]--","public int[] intersect(int[] a,int[] b){Map<Integer,Integer>m=new HashMap<>();for(int x:a)m.merge(x,1,Integer::sum);List<Integer>r=new ArrayList<>();for(int x:b){if(m.getOrDefault(x,0)>0){r.add(x);m.merge(x,-1,Integer::sum);}}return r.stream().mapToInt(i->i).toArray();}",["[1,2,2,1],[2,2]→[2,2]","No intersection → []","Same arrays → copy"],"Frequency map ensures duplicates are handled correctly. If arrays are sorted, use two-pointer approach instead for O(1) space."),
(83,"Plus One","Easy","Arrays","Given array of digits representing integer, add one.",["[1,2,3] → [1,2,4]","[9,9,9] → [1,0,0,0]"],"Process from right, handle carry. If carry out, prepend 1.","O(n) time | O(n) space for result","for i from n-1 to 0:\n  if digits[i]<9: digits[i]++; return\n  digits[i]=0\nprepend 1","public int[] plusOne(int[] d){for(int i=d.length-1;i>=0;i--){if(d[i]<9){d[i]++;return d;}d[i]=0;}int[]r=new int[d.length+1];r[0]=1;return r;}",["[1,2,3]→[1,2,4]","[9,9,9]→[1,0,0,0]","[9]→[1,0]"],"Carry propagation from right. The only case requiring extra space is all 9s — then we need a new array one size larger."),
(84,"Minimum Path Sum","Medium","DP","Find minimum path sum from top-left to bottom-right in m×n grid (only right or down).",["[[1,3,1],[1,5,1],[4,2,1]] → 7"],"DP: dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]. Can modify grid in-place.","O(m×n) time | O(1) space (in-place)","for each cell:\n  grid[i][j] += min(\n    grid[i-1][j] if exists else INF,\n    grid[i][j-1] if exists else INF)","public int minPathSum(int[][] g){int m=g.length,n=g[0].length;for(int i=0;i<m;i++)for(int j=0;j<n;j++){if(i==0&&j==0)continue;int up=i>0?g[i-1][j]:Integer.MAX_VALUE;int left=j>0?g[i][j-1]:Integer.MAX_VALUE;g[i][j]+=Math.min(up,left);}return g[m-1][n-1];}",["[[1,3,1],[1,5,1],[4,2,1]]→7","1×1 → that cell","1 row → sum of row"],"Grid DP: optimal path to each cell depends only on the cell above and to the left. In-place modification avoids O(mn) extra space."),
(85,"Unique Paths","Medium","DP","Count unique paths from top-left to bottom-right of m×n grid (right/down only).",["m=3,n=7 → 28","m=3,n=2 → 3"],"DP or combinatorics: C(m+n-2, m-1). DP fills grid row by row.","O(m×n) time | O(n) space","dp=[1]*n\nfor i in 1..m-1:\n  for j in 1..n-1:\n    dp[j]+=dp[j-1]","public int uniquePaths(int m,int n){int[]dp=new int[n];Arrays.fill(dp,1);for(int i=1;i<m;i++)for(int j=1;j<n;j++)dp[j]+=dp[j-1];return dp[n-1];}",["m=3,n=7→28","m=1,n=1→1","m=1,n=any→1"],"Combinatorially: choosing m-1 down moves out of m+n-2 total = C(m+n-2,m-1). The DP computes Pascal's triangle implicitly."),
(86,"Counting Bits","Easy","DP / Bit Manipulation","For each i in [0,n], count number of 1-bits.",["n=5 → [0,1,1,2,1,2]"],"dp[i] = dp[i>>1] + (i&1): shift right is same number without last bit, plus last bit.","O(n) time | O(n) space","dp[0]=0\nfor i in 1..n: dp[i]=dp[i>>1]+(i&1)","public int[] countBits(int n){int[]dp=new int[n+1];for(int i=1;i<=n;i++)dp[i]=dp[i>>1]+(i&1);return dp;}",["n=2→[0,1,1]","n=5→[0,1,1,2,1,2]","n=0→[0]"],"Elegant bit DP: i>>1 is i with its last bit dropped (same as floor(i/2)). Its bit count is already computed, just add the last bit."),
(87,"Find the Duplicate Number","Medium","Linked List Cycle / Floyd","Given n+1 integers in [1,n], find duplicate using O(1) space.",["[1,3,4,2,2] → 2","[3,1,3,4,2] → 3"],"Treat as linked list with cycles: nums[i] points to nums[nums[i]]. Find cycle entry using Floyd's algorithm.","O(n) time | O(1) space","slow=fast=nums[0]\nrepeat: slow=nums[slow]; fast=nums[nums[fast]]\nuntil slow==fast\nslow=nums[0]\nwhile slow!=fast: slow=nums[slow]; fast=nums[fast]","public int findDuplicate(int[] n){int slow=n[0],fast=n[0];do{slow=n[slow];fast=n[n[fast]];}while(slow!=fast);slow=n[0];while(slow!=fast){slow=n[slow];fast=n[fast];}return slow;}",["[1,3,4,2,2]→2","[3,1,3,4,2]→3","Multiple occurrences → same answer"],"Brilliant reduction: the array defines a function f(i)=nums[i]. The duplicate value creates a cycle. Floyd's algorithm finds the cycle entry — which is the duplicate."),
(88,"Palindrome Linked List","Easy","Linked List","Check if linked list is a palindrome in O(n) time and O(1) space.",["1→2→2→1 → true","1→2 → false"],"Find middle (slow/fast pointer), reverse second half, compare with first half.","O(n) time | O(1) space","mid=findMiddle(head)\nsecond=reverse(mid.next)\np1=head; p2=second\nwhile p2: if p1.val!=p2.val: return false\nreturn true","public boolean isPalindrome(ListNode h){ListNode s=h,f=h;while(f!=null&&f.next!=null){s=s.next;f=f.next.next;}ListNode p=null,c=s;while(c!=null){ListNode n=c.next;c.next=p;p=c;c=n;}while(p!=null){if(h.val!=p.val)return false;h=h.next;p=p.next;}return true;}",["1→2→2→1 → true","1→2 → false","Single node → true"],"Combines three techniques: slow/fast pointer for midpoint, in-place reversal, then comparison. O(1) space by operating on the list itself."),
(89,"Maximum Product Subarray","Medium","DP","Find subarray with maximum product.",["[2,3,-2,4] → 6","[-2,0,-1] → 0"],"Track both max and min product ending at current position (negatives can flip max to min).","O(n) time | O(1) space","curMax=curMin=result=nums[0]\nfor n in nums[1:]:\n  candidates=(n, curMax*n, curMin*n)\n  curMax=max(candidates)\n  curMin=min(candidates)\n  result=max(result,curMax)","public int maxProduct(int[] n){int max=n[0],min=n[0],res=n[0];for(int i=1;i<n.length;i++){int t=max;max=Math.max(n[i],Math.max(max*n[i],min*n[i]));min=Math.min(n[i],Math.min(t*n[i],min*n[i]));res=Math.max(res,max);}return res;}",["[2,3,-2,4]→6","[-2,0,-1]→0","[-2,-3,-4]→12"],"Negative × negative = positive, so track both max and min. A single negative can turn today's minimum into tomorrow's maximum."),
(90,"Implement Stack using Queues","Easy","Stack/Queue","Implement stack using only queue operations.",["push(1),push(2),top()→2,pop()→2,empty()→false"],"On push: enqueue, then rotate all previous elements to back. O(n) push, O(1) pop.","O(n) push | O(1) pop and top","push(x): enqueue x, then dequeue and re-enqueue n-1 times (x is now at front)","public class MyStack{Queue<Integer>q=new LinkedList<>();public void push(int x){q.offer(x);for(int i=1;i<q.size();i++)q.offer(q.poll());}public int pop(){return q.poll();}public int top(){return q.peek();}public boolean empty(){return q.isEmpty();}}",["push(1),push(2),top()→2","pop then empty()→true"],"Rotating the queue after each push ensures LIFO order — the newest element is always at the front."),
(91,"Design HashMap","Easy","Design","Design a HashMap with put, get, remove using an array of linked lists (chaining).",["put(1,1),put(2,2),get(1)→1,remove(2),get(2)→-1"],"Array of 1000 buckets, each a linked list. Hash key to bucket, chain collisions.","O(1) amortised | O(n) space","buckets=[[]]*SIZE\nhash(key)=key%SIZE\nput: find bucket, update or append\nget: find bucket, linear search","public class MyHashMap{LinkedList<int[]>[]m;public MyHashMap(){m=new LinkedList[1024];for(int i=0;i<1024;i++)m[i]=new LinkedList<>();}int h(int k){return k%1024;}public void put(int k,int v){int b=h(k);for(int[]p:m[b])if(p[0]==k){p[1]=v;return;}m[b].add(new int[]{k,v});}public int get(int k){for(int[]p:m[h(k)])if(p[0]==k)return p[1];return -1;}public void remove(int k){m[h(k)].removeIf(p->p[0]==k);}}",["put/get/remove basic ops","Key collisions handled","Overwrite existing key"],"Hash table fundamentals: hash function maps key to bucket, chaining resolves collisions. Load factor determines when to resize (not shown here for simplicity)."),
(92,"Reverse Words in a String","Medium","String","Given a string, reverse the order of words.",["'the sky is blue' → 'blue is sky the'","'  hello world  ' → 'world hello'"],"Split by spaces, filter empty, reverse the list, join.","O(n) time | O(n) space","words=s.trim().split()  // handle multiple spaces\nreturn reversed(words).join(' ')","public String reverseWords(String s){String[]w=s.trim().split(\"\\\\s+\");StringBuilder sb=new StringBuilder();for(int i=w.length-1;i>=0;i--){sb.append(w[i]);if(i>0)sb.append(' ');}return sb.toString();}",["'the sky is blue'→'blue is sky the'","Multiple spaces handled","Leading/trailing spaces trimmed"],"\\s+ regex splits on any whitespace sequence. In-place solution: reverse entire string, then reverse each word individually — O(1) extra space."),
(93,"Isomorphic Strings","Easy","HashMap","Two strings are isomorphic if characters can be mapped one-to-one.",["s='egg',t='add' → true","s='foo',t='bar' → false"],"Maintain two maps: s→t char mapping and t→s reverse mapping. Check consistency.","O(n) time | O(1) space (bounded charset)","s2t={}, t2s={}\nfor sc,tc in zip(s,t):\n  if s2t.get(sc,tc)!=tc or t2s.get(tc,sc)!=sc: return false\n  s2t[sc]=tc; t2s[tc]=sc","public boolean isIsomorphic(String s,String t){Map<Character,Character>st=new HashMap<>(),ts=new HashMap<>();for(int i=0;i<s.length();i++){char a=s.charAt(i),b=t.charAt(i);if(st.containsKey(a)&&st.get(a)!=b)return false;if(ts.containsKey(b)&&ts.get(b)!=a)return false;st.put(a,b);ts.put(b,a);}return true;}",["'egg','add'→true","'foo','bar'→false","'paper','title'→true","'ab','aa'→false"],"Bidirectional mapping ensures no two characters in s map to same character in t, and vice versa. Using only positions (first occurrence index) is an elegant alternative."),
(94,"Ransom Note","Easy","HashMap","Check if ransomNote can be constructed from magazine letters.",["ransomNote='a', magazine='b' → false","ransomNote='aa', magazine='aab' → true"],"Count magazine letters, subtract ransom letters. Return false if any goes negative.","O(n) time | O(1) space (26 letters)","count=int[26]; fill from magazine\nfor c in ransomNote: if count[c-'a']--<0: return false\nreturn true","public boolean canConstruct(String r,String m){int[]c=new int[26];for(char x:m.toCharArray())c[x-'a']++;for(char x:r.toCharArray())if(--c[x-'a']<0)return false;return true;}",["'a','b'→false","'aa','aab'→true","'aab','baa'→true"],"Character frequency array (size 26) gives O(1) space. Decrement on use; negative count means insufficient letters."),
(95,"Valid Anagram","Easy","HashMap","Check if t is an anagram of s.",["s='anagram',t='nagaram' → true","s='rat',t='car' → false"],"Count character frequencies. Same counts = anagram.","O(n) time | O(1) space","count=int[26]\nfor c in s: count[c-'a']++\nfor c in t: count[c-'a']--\nreturn all(count)==0","public boolean isAnagram(String s,String t){if(s.length()!=t.length())return false;int[]c=new int[26];for(char x:s.toCharArray())c[x-'a']++;for(char x:t.toCharArray())if(--c[x-'a']<0)return false;return true;}",["'anagram','nagaram'→true","'rat','car'→false","Different lengths→false"],"Frequency counting is the canonical anagram check. Sorting both strings also works but is O(n log n). For Unicode, use HashMap instead of fixed-size array."),
(96,"First Unique Character","Easy","HashMap","Find first non-repeating character in string.",["'leetcode' → 0","'loveleetcode' → 2"],"Count all character frequencies first. Then find first character with count 1.","O(n) time | O(1) space","count=frequency map\nfor i,c in enumerate(s): if count[c]==1: return i\nreturn -1","public int firstUniqChar(String s){int[]c=new int[26];for(char x:s.toCharArray())c[x-'a']++;for(int i=0;i<s.length();i++)if(c[s.charAt(i)-'a']==1)return i;return -1;}",["'leetcode'→0","'aabb'→-1","'z'→0"],"Two-pass approach: first build full frequency map, then scan for first count-1 character. One-pass with order-preserving map is also possible."),
(97,"Path Sum","Easy","Trees","Given binary tree root and targetSum, return true if any root-to-leaf path sums to targetSum.",["root=[5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum=22 → true"],"DFS: subtract node value from target, return true at leaf if target reaches 0.","O(n) time | O(h) space","function hasPathSum(node, target):\n  if node==null: return false\n  if leaf and node.val==target: return true\n  return hasPathSum(left, target-node.val) or hasPathSum(right, target-node.val)","public boolean hasPathSum(TreeNode r,int t){if(r==null)return false;t-=r.val;if(r.left==null&&r.right==null)return t==0;return hasPathSum(r.left,t)||hasPathSum(r.right,t);}",["Target matches leaf→true","Target doesn't match→false","Empty tree→false"],"Subtract-and-check DFS: decrement target as we descend. At leaf, check if exactly consumed. No need to track full path."),
(98,"Symmetric Tree","Easy","Trees","Check if a binary tree is a mirror of itself.",["[1,2,2,3,4,4,3] → true","[1,2,2,null,3,null,3] → false"],"Recursive: check if left subtree mirrors right subtree. Mirror: outer values equal and inner subtrees mirror each other.","O(n) time | O(h) space","function isMirror(l,r):\n  if both null: return true\n  if one null: return false\n  return l.val==r.val and isMirror(l.left,r.right) and isMirror(l.right,r.left)","public boolean isSymmetric(TreeNode r){return check(r,r);}boolean check(TreeNode a,TreeNode b){if(a==null&&b==null)return true;if(a==null||b==null)return false;return a.val==b.val&&check(a.left,b.right)&&check(a.right,b.left);}",["Perfect mirror→true","Off by one node→false","Single node→true"],"Mirror check crosses subtrees: left-left mirrors right-right, left-right mirrors right-left. BFS level-by-level comparison also works."),
(99,"Invert Binary Tree","Easy","Trees","Invert a binary tree (mirror reflection).",["[4,2,7,1,3,6,9] → [4,7,2,9,6,3,1]"],"Recursive post-order: invert left, invert right, swap them.","O(n) time | O(h) space","function invert(root):\n  if root==null: return null\n  root.left, root.right = invert(root.right), invert(root.left)\n  return root","public TreeNode invertTree(TreeNode r){if(r==null)return null;TreeNode t=r.left;r.left=invertTree(r.right);r.right=invertTree(t);return r;}",["[4,2,7,1,3,6,9]→[4,7,2,9,6,3,1]","Single node→unchanged","Null→null"],"The tweet that launched a thousand interviews: homebrew solution from Max Howell. Post-order recursion elegantly swaps every pair of children."),
(100,"Diameter of Binary Tree","Easy","Trees","Find length of longest path between any two nodes in tree.",["[1,2,3,4,5] → 3 (path: 4→2→1→3 or 5→2→1→3)"],"DFS: at each node, diameter through it = left_depth + right_depth. Track global maximum.","O(n) time | O(h) space","maxDiam=0\nfunction depth(node):\n  if null: return 0\n  l=depth(left); r=depth(right)\n  maxDiam=max(maxDiam, l+r)\n  return 1+max(l,r)","public int diameterOfBinaryTree(TreeNode r){int[]max={0};depth(r,max);return max[0];}int depth(TreeNode n,int[]max){if(n==null)return 0;int l=depth(n.left,max),ri=depth(n.right,max);max[0]=Math.max(max[0],l+ri);return 1+Math.max(l,ri);}",["[1,2,3,4,5]→3","Single node→0","Linear tree→n-1"],"Diameter = max over all nodes of (left_height + right_height). The path doesn't have to pass through root. Same pattern as Binary Tree Maximum Path Sum — dual-purpose DFS."),
]

for e in short_probs:
    problems.append(e)

# ════════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ════════════════════════════════════════════════════════════════════════════

story = []

# ── Cover page ───────────────────────────────────────────────────────────────
cover_data = [[Paragraph("Comprehensive DSA<br/>Practice Guide", ST["title"])]]
cover_tbl = Table(cover_data, colWidths=[WIDTH - 3.6*cm])
cover_tbl.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), C_DARK),
    ("TOPPADDING",(0,0),(-1,-1),40),
    ("BOTTOMPADDING",(0,0),(-1,-1),40),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),
]))
story.append(cover_tbl)
story.append(sp(16))

subtitle_data = [[Paragraph("100 LeetCode Problems · Java Solutions · From Basic to Advanced", ST["subtitle"])]]
s_tbl = Table(subtitle_data, colWidths=[WIDTH - 3.6*cm])
s_tbl.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), HexColor("#16213e")),
    ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),
]))
story.append(s_tbl)
story.append(sp(20))

badges = [["Arrays","Two Pointers","Sliding Window","Stack","Queue"],
          ["Linked List","Binary Search","Trees","Graphs","Dynamic Programming"],
          ["Backtracking","Heap","Trie","Union-Find","Sorting"],
          ["Segment Tree","Dijkstra","Bellman-Ford","Topological Sort","Bit Manip"]]
for row in badges:
    cells = [[Paragraph(f"<b>{t}</b>",
              ParagraphStyle("badge",parent=SS["Normal"],fontSize=8,textColor=C_WHITE,
                             alignment=TA_CENTER,leading=10))] for t in row]
    btbl = Table([cells], colWidths=[(WIDTH-3.6*cm)/5]*5)
    btbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), C_ACCENT),
        ("GRID",(0,0),(-1,-1),1,C_DARK),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(btbl)
    story.append(sp(2))
story.append(PageBreak())

# ── Introduction ─────────────────────────────────────────────────────────────
story.append(chapter_header("INTRODUCTION TO DSA"))
story.append(sp(8))
intro = [
("What is DSA?",
 "Data Structures and Algorithms (DSA) is the backbone of computer science. Data structures organise data for efficient access and modification. Algorithms define step-by-step procedures to solve problems using those structures. Together they determine the performance of every software system."),
("Why Learn DSA?",
 "Mastering DSA is essential for technical interviews at leading technology companies. More importantly, it builds rigorous problem-solving skills that improve code quality across all domains. Problems that seem complex often reduce to well-known patterns once you recognise the underlying structure."),
("How to Use This Guide",
 "Problems are grouped by topic and progress from Easy to Hard within each section. For every problem, study the Approach before looking at code — understanding the 'why' is more valuable than memorising the 'what'. Pay special attention to Conceptual Insights, which highlight transferable patterns."),
("Complexity Analysis",
 "Every solution includes Time and Space complexity. Big-O notation describes worst-case growth. Common complexities from fastest to slowest: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n²) quadratic, O(2^n) exponential, O(n!) factorial."),
("Problem-Solving Framework",
 "1. Understand: Restate the problem in your own words. 2. Examples: Trace through given examples and create your own. 3. Brute Force: Find a naive correct solution first. 4. Optimise: Identify bottlenecks (usually the innermost loop). 5. Code: Implement cleanly. 6. Test: Edge cases — empty, single element, maximum values."),
]
for title_t, text in intro:
    story.append(hline(C_TEAL,0.5))
    story.append(Paragraph(f"<b>{title_t}</b>", ST["label"]))
    story.append(body(text))
    story.append(sp(4))
story.append(PageBreak())

# ── TOC ───────────────────────────────────────────────────────────────────────
story.append(chapter_header("TABLE OF CONTENTS"))
story.append(sp(10))
toc_entries = [
    ("Arrays & Strings", [f"#{i} {t}" for i,t in [(1,"Two Sum"),(2,"Best Time Buy/Sell Stock"),(3,"Contains Duplicate"),(4,"Product Except Self"),(5,"Maximum Subarray"),(6,"Merge Intervals")]]),
    ("Two Pointers & Sliding Window", [f"#{i} {t}" for i,t in [(7,"Valid Palindrome"),(8,"3Sum"),(9,"Longest Substring No Repeat"),(10,"Minimum Window Substring")]]),
    ("Stacks & Queues", [f"#{i} {t}" for i,t in [(11,"Valid Parentheses"),(12,"Daily Temperatures"),(13,"Queue using Stacks")]]),
    ("Linked Lists", [f"#{i} {t}" for i,t in [(14,"Reverse Linked List"),(15,"Merge Two Sorted Lists"),(16,"Detect Cycle"),(17,"LRU Cache")]]),
    ("Binary Search", [f"#{i} {t}" for i,t in [(18,"Binary Search"),(19,"Find Min Rotated"),(20,"Search Rotated")]]),
    ("Trees & BST", [f"#{i} {t}" for i,t in [(21,"Max Depth"),(22,"Validate BST"),(23,"Level Order"),(24,"Max Path Sum")]]),
    ("Graph Algorithms", [f"#{i} {t}" for i,t in [(25,"Number of Islands"),(26,"Clone Graph"),(27,"Course Schedule"),(28,"Word Ladder")]]),
    ("Dynamic Programming", [f"#{i} {t}" for i,t in [(29,"Climbing Stairs"),(30,"Coin Change"),(31,"LCS"),(32,"0/1 Knapsack"),(33,"Word Break"),(34,"Edit Distance")]]),
    ("Backtracking", [f"#{i} {t}" for i,t in [(35,"Subsets"),(36,"Permutations"),(37,"N-Queens")]]),
    ("Heap & Priority Queue", [f"#{i} {t}" for i,t in [(38,"Top K Frequent"),(39,"Median from Stream")]]),
    ("Trie", ["#40 Implement Trie"]),
    ("Advanced Graphs", [f"#{i} {t}" for i,t in [(41,"Network Delay (Dijkstra)"),(42,"Cheapest Flights (Bellman-Ford)")]]),
    ("Union-Find", ["#43 Connected Components"]),
    ("Sorting", [f"#{i} {t}" for i,t in [(44,"Merge Sort"),(45,"Quick Sort")]]),
    ("Advanced DS & Algorithms", [f"#{i} {t}" for i,t in [(46,"Segment Tree"),(47,"Kruskal MST"),(48,"Topological Sort"),(49,"LIS"),(50,"Serialize Binary Tree")]]),
    ("Additional Problems #51–100", ["Arrays, Math, Bit Manipulation, Greedy, String, Trees"]),
]
for ch, items in toc_entries:
    story.append(Paragraph(ch, ST["toc_ch"]))
    for item in items:
        story.append(Paragraph(f"• {item}", ST["toc_item"]))
story.append(PageBreak())

# ── Problems ──────────────────────────────────────────────────────────────────
current_section = None
prob_count = 0

for entry in problems:
    if len(entry) == 3 and entry[1] is None:
        # Section header
        if prob_count > 0:
            story.append(PageBreak())
        story.append(chapter_header(entry[0]))
        story.append(sp(8))
        current_section = entry[0]
        prob_count = 0
    else:
        if len(entry) == 13:
            num,title,diff,cat,stmt,exs,appr,comp,pseudo,java,tests,insight_t = entry[1:]
            num = entry[0]
        else:
            num,title,diff,cat,stmt,exs,appr,comp,pseudo,java,tests,insight_t = entry
        elems = problem(num,title,diff,cat,stmt,exs,appr,comp,pseudo,java,tests,insight_t)
        story.extend(elems)
        prob_count += 1

# ── Appendix: Quick Reference ─────────────────────────────────────────────────
story.append(PageBreak())
story.append(chapter_header("APPENDIX: QUICK REFERENCE"))
story.append(sp(8))

complexity_data = [
    ["Algorithm/Structure", "Average Time", "Worst Time", "Space"],
    ["Array Access", "O(1)", "O(1)", "O(n)"],
    ["Hash Map Get/Put", "O(1)", "O(n)", "O(n)"],
    ["Binary Search", "O(log n)", "O(log n)", "O(1)"],
    ["DFS / BFS", "O(V+E)", "O(V+E)", "O(V)"],
    ["Merge Sort", "O(n log n)", "O(n log n)", "O(n)"],
    ["Quick Sort", "O(n log n)", "O(n²)", "O(log n)"],
    ["Heap Insert/Remove", "O(log n)", "O(log n)", "O(n)"],
    ["Trie Insert/Search", "O(L)", "O(L)", "O(N·L)"],
    ["Dijkstra (min-heap)", "O((V+E)log V)", "O((V+E)log V)", "O(V+E)"],
    ["Bellman-Ford", "O(VE)", "O(VE)", "O(V)"],
    ["Union-Find (w/ PC)", "O(α(n))", "O(α(n))", "O(n)"],
    ["Segment Tree", "O(log n)", "O(log n)", "O(n)"],
]
col_w = [(WIDTH-3.6*cm)/4]*4
ct = Table(complexity_data, colWidths=col_w)
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), C_PRIMARY),
    ("TEXTCOLOR",(0,0),(-1,0), C_WHITE),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("FONTSIZE",(0,0),(-1,-1),8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE, C_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.5,HexColor("#dee2e6")),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("ALIGN",(1,0),(-1,-1),"CENTER"),
]))
story.append(ct)
story.append(sp(12))
story.append(insight_box("PC = Path Compression, α = Inverse Ackermann (practically O(1)), L = string length, N = number of strings, V = vertices, E = edges"))
story.append(sp(8))

patterns = [
    ("Two Pointers", "Sorted array problems, palindromes, pair sums. Move toward each other or in same direction."),
    ("Sliding Window", "Substring/subarray problems with a constraint. Expand right, shrink left when violated."),
    ("Fast & Slow Pointer", "Cycle detection, finding midpoint, palindrome linked list."),
    ("Merge Intervals", "Sort by start, then linearly merge overlapping pairs."),
    ("Cyclic Sort", "Arrays with values in range [1..n]. Place each number at its index."),
    ("Monotonic Stack", "Next greater/smaller element problems. Maintain stack with monotone property."),
    ("HashMap + Problem", "Frequency counting, two-sum pattern, cache, grouping."),
    ("BFS for Shortest Path", "Unweighted graph or level-by-level tree traversal."),
    ("DFS for Connected Components", "Flood fill, island counting, graph traversal."),
    ("DP (1D/2D)", "Overlapping subproblems + optimal substructure. Identify state, transition, base case."),
    ("Backtracking Template", "Explore → recurse → undo. Prune early for efficiency."),
    ("Divide & Conquer", "Split problem in half, solve independently, merge."),
    ("Greedy", "Make locally optimal choice at each step. Prove it leads to global optimum."),
    ("Bit Manipulation", "XOR for duplicates, AND/OR for masking, n&(n-1) to clear lowest bit."),
]
story.append(Paragraph("<b>PATTERN RECOGNITION GUIDE</b>", ST["label"]))
story.append(sp(4))
for pname, pdesc in patterns:
    row = [[Paragraph(f"<b>{pname}</b>", ParagraphStyle("pn",parent=SS["Normal"],fontSize=8.5,textColor=C_ACCENT,fontName="Helvetica-Bold")),
            Paragraph(pdesc, ST["body"])]]
    pt = Table(row, colWidths=[3.5*cm, WIDTH-3.6*cm-3.5*cm])
    pt.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LINEBELOW",(0,0),(-1,-1),0.3,HexColor("#dee2e6")),
    ]))
    story.append(pt)

# ── Back cover ────────────────────────────────────────────────────────────────
story.append(PageBreak())
back_data = [[Paragraph("Keep practising.<br/>Consistency beats intensity.<br/>Good luck!", ST["title"])]]
bt = Table(back_data, colWidths=[WIDTH-3.6*cm])
bt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), C_DARK),
    ("TOPPADDING",(0,0),(-1,-1),60),("BOTTOMPADDING",(0,0),(-1,-1),60),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),
]))
story.append(sp(60))
story.append(bt)

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF generated successfully!")